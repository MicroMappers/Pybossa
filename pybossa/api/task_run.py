# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2014 SF Isle of Man Limited
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
PyBossa api module for exposing domain object TaskRun via an API.

This package adds GET, POST, PUT and DELETE methods for:
    * task_runs

"""
from flask import request
from flask.ext.login import current_user
from pybossa.model.task_run import TaskRun
from werkzeug.exceptions import Forbidden, BadRequest

from api_base import APIBase
from pybossa.util import get_user_id_or_ip
from pybossa.core import task_repo, sentinel


class TaskRunAPI(APIBase):

    """Class API for domain object TaskRun."""

    __class__ = TaskRun
    reserved_keys = set(['id', 'created', 'finish_time'])

    def _update_object(self, taskrun):
        """Update task_run object with user id or ip."""
        # validate the task and project for that taskrun are ok
        task = task_repo.get_task(taskrun.task_id)
        if task is None:  # pragma: no cover
            raise Forbidden('Invalid task_id')
        if (task.project_id != taskrun.project_id):
            raise Forbidden('Invalid project_id')
        if _check_task_requested_by_user(taskrun, sentinel.master) is False:
            raise Forbidden('You must request a task first!')

        # Add the user info so it cannot post again the same taskrun

        if current_user.is_anonymous():
            taskrun.user_ip = request.remote_addr
        else:
            taskrun.user_id = current_user.id

        if request.headers.get('remote_mobile_addr') is not None :
                taskrun.user_ip = request.headers.get('remote_mobile_addr') if current_user.is_anonymous() else None
        else:
                if request.headers.getlist("X-Forwarded-For"):
                    user_ip = request.headers.getlist("X-Forwarded-For")[0]
                    taskrun.user_ip = user_ip


        print "user_ip %s." % user_ip
        if ',' in user_ip:
                ips = user_ip.split(",")
                for ip in ips:
                    taskrun.user_ip = ip

        print "taskrun.user_ip %s." % taskrun.user_ip

    def _forbidden_attributes(self, data):
        for key in data.keys():
            if key in self.reserved_keys:
                raise BadRequest("Reserved keys in payload")


def _check_task_requested_by_user(taskrun, redis_conn):
    user_id_ip = get_user_id_or_ip()
    usr = user_id_ip['user_id'] or user_id_ip['user_ip']
    key = 'pybossa:task_requested:user:%s:task:%s' % (usr, taskrun.task_id)
    task_requested = bool(redis_conn.get(key))
    if user_id_ip['user_id'] is not None:
        redis_conn.delete(key)
    return task_requested
