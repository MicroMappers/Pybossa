# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2013 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.
"""
PyBossa api module for exposing domain objects via an API.

This package adds GET, POST, PUT and DELETE methods for any class:
    * projects,
    * tasks,
    * task_runs,
    * users,
    * etc.

"""
import json
from flask import request, abort, Response
from flask.views import MethodView
from werkzeug.exceptions import NotFound, Unauthorized, Forbidden
from pybossa.util import jsonpify, crossdomain
from pybossa.core import ratelimits
from pybossa.auth import ensure_authorized_to
from pybossa.hateoas import Hateoas
from pybossa.ratelimit import ratelimit
from pybossa.error import ErrorStatus
from pybossa.core import project_repo, user_repo, task_repo

repos = {'Task'   : {'repo': task_repo, 'filter': 'filter_tasks_by',
                     'get': 'get_task', 'save': 'save', 'update': 'update',
                     'delete': 'delete'},
        'TaskRun' : {'repo': task_repo, 'filter': 'filter_task_runs_by',
                     'get': 'get_task_run',  'save': 'save', 'update': 'update',
                     'delete': 'delete'},
        'User'    : {'repo': user_repo, 'filter': 'filter_by', 'get': 'get',
                     'save': 'save', 'update': 'update'},
        'Project' : {'repo': project_repo, 'filter': 'filter_by', 'get': 'get',
                     'save': 'save', 'update': 'update', 'delete': 'delete'},
        'Category': {'repo': project_repo, 'filter': 'filter_categories_by',
                     'get': 'get_category', 'save': 'save_category',
                     'update': 'update_category', 'delete': 'delete_category'}
        }


cors_headers = ['Content-Type', 'Authorization']

error = ErrorStatus()


class APIBase(MethodView):

    """Class to create CRUD methods."""

    hateoas = Hateoas()

    def valid_args(self):
        """Check if the domain object args are valid."""
        for k in request.args.keys():
            if k not in ['api_key']:
                getattr(self.__class__, k)

    @crossdomain(origin='*', headers=cors_headers)
    def options(self):  # pragma: no cover
        """Return '' for Options method."""
        return ''

    @jsonpify
    @crossdomain(origin='*', headers=cors_headers)
    @ratelimit(limit=ratelimits.get('LIMIT'), per=ratelimits.get('PER'))
    def get(self, oid):
        """Get an object.

        Returns an item from the DB with the request.data JSON object or all
        the items if oid == None

        :arg self: The class of the object to be retrieved
        :arg integer oid: the ID of the object in the DB
        :returns: The JSON item/s stored in the DB

        """
        try:
            ensure_authorized_to('read', self.__class__)
            query = self._db_query(oid)
            json_response = self._create_json_response(query, oid)
            return Response(json_response, mimetype='application/json')
        except Exception as e:
            return error.format_exception(
                e,
                target=self.__class__.__name__.lower(),
                action='GET')

    def _create_json_response(self, query_result, oid):
        if len (query_result) == 1 and query_result[0] is None:
            raise abort(404)
        items = []
        for item in query_result:
            try:
                items.append(self._create_dict_from_model(item))
                ensure_authorized_to('read', item)
            except (Forbidden, Unauthorized):
                # Remove last added item, as it is 401 or 403
                items.pop()
            except Exception:  # pragma: no cover
                raise
        if oid is not None:
            ensure_authorized_to('read', query_result[0])
            items = items[0]
        return json.dumps(items)

    def _create_dict_from_model(self, model):
        return self._select_attributes(self._add_hateoas_links(model))

    def _add_hateoas_links(self, item):
        obj = item.dictize()
        links, link = self.hateoas.create_links(item)
        if links:
            obj['links'] = links
        if link:
            obj['link'] = link
        return obj

    def _db_query(self, oid):
        """Returns a list with the results of the query"""
        repo_info = repos[self.__class__.__name__]
        if oid is None:
            limit, offset = self._set_limit_and_offset()
            results = self._filter_query(repo_info, limit, offset)
        else:
            repo = repo_info['repo']
            query_func = repo_info['get']
            results = [getattr(repo, query_func)(oid)]
        return results

    def _filter_query(self, repo_info, limit, offset):
        filters = {}
        for k in request.args.keys():
            if k not in ['limit', 'offset', 'api_key', 'last_id']:
                # Raise an error if the k arg is not a column
                getattr(self.__class__, k)
                filters[k] = request.args[k]
        repo = repo_info['repo']
        query_func = repo_info['filter']
        filters = self._custom_filter(filters)
        last_id = request.args.get('last_id')
        if last_id:
            results = getattr(repo, query_func)(limit=limit, last_id=last_id,
                                                **filters)
        else:
            results = getattr(repo, query_func)(limit=limit, offset=offset,
                                                **filters)
        return results

    def _set_limit_and_offset(self):
        try:
            limit = min(100, int(request.args.get('limit')))
        except (ValueError, TypeError):
            limit = 20
        try:
            offset = int(request.args.get('offset'))
        except (ValueError, TypeError):
            offset = 0
        return limit, offset

    @jsonpify
    @crossdomain(origin='*', headers=cors_headers)
    @ratelimit(limit=ratelimits.get('LIMIT'), per=ratelimits.get('PER'))
    def post(self):
        """Post an item to the DB with the request.data JSON object.

        :arg self: The class of the object to be inserted
        :returns: The JSON item stored in the DB

        """
        try:
            self.valid_args()
            data = json.loads(request.data)
            self._forbidden_attributes(data)
            inst = self._create_instance_from_request(data)
            repo = repos[self.__class__.__name__]['repo']
            save_func = repos[self.__class__.__name__]['save']
            getattr(repo, save_func)(inst)
            self._log_changes(None, inst)
            return json.dumps(inst.dictize())
        except Exception as e:
            return error.format_exception(
                e,
                target=self.__class__.__name__.lower(),
                action='POST')

    def _create_instance_from_request(self, data):
        data = self.hateoas.remove_links(data)
        inst = self.__class__(**data)
        self._update_object(inst)
        ensure_authorized_to('create', inst)
        self._validate_instance(inst)
        return inst

    @jsonpify
    @crossdomain(origin='*', headers=cors_headers)
    @ratelimit(limit=ratelimits.get('LIMIT'), per=ratelimits.get('PER'))
    def delete(self, oid):
        """Delete a single item from the DB.

        :arg self: The class of the object to be deleted
        :arg integer oid: the ID of the object in the DB
        :returns: An HTTP status code based on the output of the action.

        More info about HTTP status codes for this action `here
        <http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7>`_.

        """
        try:
            self.valid_args()
            self._delete_instance(oid)
            return '', 204
        except Exception as e:
            return error.format_exception(
                e,
                target=self.__class__.__name__.lower(),
                action='DELETE')

    def _delete_instance(self, oid):
        repo = repos[self.__class__.__name__]['repo']
        query_func = repos[self.__class__.__name__]['get']
        inst = getattr(repo, query_func)(oid)
        if inst is None:
            raise NotFound
        ensure_authorized_to('delete', inst)
        self._log_changes(inst, None)
        delete_func = repos[self.__class__.__name__]['delete']
        getattr(repo, delete_func)(inst)
        return inst

    @jsonpify
    @crossdomain(origin='*', headers=cors_headers)
    @ratelimit(limit=ratelimits.get('LIMIT'), per=ratelimits.get('PER'))
    def put(self, oid):
        """Update a single item in the DB.

        :arg self: The class of the object to be updated
        :arg integer oid: the ID of the object in the DB
        :returns: An HTTP status code based on the output of the action.

        More info about HTTP status codes for this action `here
        <http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.6>`_.

        """
        try:
            self.valid_args()
            inst = self._update_instance(oid)
            return Response(json.dumps(inst.dictize()), 200,
                            mimetype='application/json')
        except Exception as e:
            return error.format_exception(
                e,
                target=self.__class__.__name__.lower(),
                action='PUT')

    def _update_instance(self, oid):
        repo = repos[self.__class__.__name__]['repo']
        query_func = repos[self.__class__.__name__]['get']
        existing = getattr(repo, query_func)(oid)
        if existing is None:
            raise NotFound
        ensure_authorized_to('update', existing)
        data = json.loads(request.data)
        self._forbidden_attributes(data)
        # Remove hateoas links
        data = self.hateoas.remove_links(data)
        # may be missing the id as we allow partial updates
        data['id'] = oid
        self.__class__(**data)
        old = self.__class__(**existing.dictize())
        for key in data:
            setattr(existing, key, data[key])
        update_func = repos[self.__class__.__name__]['update']
        self._validate_instance(existing)
        getattr(repo, update_func)(existing)
        self._log_changes(old, existing)
        return existing


    def _update_object(self, data_dict):
        """Update object.

        Method to be overriden in inheriting classes which wish to update
        data dict.

        """
        pass

    def _select_attributes(self, item_data):
        """Method to be overriden in inheriting classes in case it is not
        desired that every object attribute is returned by the API.
        """
        return item_data

    def _custom_filter(self, query):
        """Method to be overriden in inheriting classes which wish to consider
        specific filtering criteria.
        """
        return query

    def _validate_instance(self, instance):
        """Method to be overriden in inheriting classes which may need to
        validate the creation (POST) or modification (PUT) of a domain object for
        reasons other than business logic ones (e.g. overlapping of a project
        name witht a URL).
        """
        pass

    def _log_changes(self, old_obj, new_obj):
        """Method to be overriden by inheriting classes for logging purposes"""
        pass

    def _forbidden_attributes(self, data):
        """Method to be overriden by inheriting classes that will not allow for
        certain fields to be used in PUT or POST requests"""
        pass
