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
import json
from default import with_context
from nose.tools import assert_equal, assert_raises
from test_api import TestAPI

from factories import ProjectFactory, TaskFactory, TaskRunFactory, UserFactory



class TestApiCommon(TestAPI):


    @with_context
    def test_limits_query(self):
        """Test API GET limits works"""
        owner = UserFactory.create()
        projects = ProjectFactory.create_batch(30, owner=owner)
        for project in projects:
            task = TaskFactory.create(project=project)
            TaskRunFactory.create(task=task)

        res = self.app.get('/api/project')
        data = json.loads(res.data)
        assert len(data) == 20, len(data)

        res = self.app.get('/api/project?limit=10')
        data = json.loads(res.data)
        assert len(data) == 10, len(data)

        # DEPRECATED
        res = self.app.get('/api/project?limit=10&offset=10')
        data = json.loads(res.data)
        assert len(data) == 10, len(data)
        assert data[0].get('name') == projects[10].name, data[0]

        # Keyset pagination
        url = '/api/project?limit=10&last_id=%s' % projects[9].id
        res = self.app.get(url)
        data = json.loads(res.data)
        assert len(data) == 10, len(data)
        assert data[0].get('name') == projects[10].name, data[0]

        res = self.app.get('/api/task')
        data = json.loads(res.data)
        assert len(data) == 20, len(data)

        res = self.app.get('/api/taskrun')
        data = json.loads(res.data)
        assert len(data) == 20, len(data)

        UserFactory.create_batch(30)

        res = self.app.get('/api/user')
        data = json.loads(res.data)
        assert len(data) == 20, len(data)

        res = self.app.get('/api/user?limit=10')
        data = json.loads(res.data)
        assert len(data) == 10, len(data)

        # DEPRECATED
        res = self.app.get('/api/user?limit=10&offset=10')
        data = json.loads(res.data)
        assert len(data) == 10, len(data)
        assert data[0].get('name') == 'user11', data

        res = self.app.get('/api/user?limit=10&last_id=10')
        data = json.loads(res.data)
        assert len(data) == 10, len(data)
        assert data[0].get('name') == 'user11', data

    @with_context
    def test_get_query_with_api_key(self):
        """ Test API GET query with an API-KEY"""
        users = UserFactory.create_batch(3)
        project = ProjectFactory.create(owner=users[0], info={'total': 150})
        task = TaskFactory.create(project=project, info={'url': 'my url'})
        taskrun = TaskRunFactory.create(task=task, user=users[0],
                                        info={'answer': 'annakarenina'})
        for endpoint in self.endpoints:
            url = '/api/' + endpoint + '?api_key=' + users[1].api_key
            res = self.app.get(url)
            data = json.loads(res.data)

            if endpoint == 'project':
                assert len(data) == 1, data
                project = data[0]
                assert project['info']['total'] == 150, data
                assert res.mimetype == 'application/json', res

            if endpoint == 'task':
                assert len(data) == 1, data
                task = data[0]
                assert task['info']['url'] == 'my url', data
                assert res.mimetype == 'application/json', res

            if endpoint == 'taskrun':
                assert len(data) == 1, data
                taskrun = data[0]
                assert taskrun['info']['answer'] == 'annakarenina', data
                assert res.mimetype == 'application/json', res

            if endpoint == 'user':
                assert len(data) == 3, data
                user = data[0]
                assert user['name'] == 'user1', data
                assert res.mimetype == 'application/json', res


    @with_context
    def test_query_search_wrongfield(self):
        """ Test API query search works"""
        # Test first a non-existant field for all end-points
        for endpoint in self.endpoints:
            res = self.app.get("/api/%s?wrongfield=value" % endpoint)
            err = json.loads(res.data)
            assert res.status_code == 415, err
            assert err['status'] == 'failed', err
            assert err['action'] == 'GET', err
            assert err['exception_cls'] == 'AttributeError', err


    @with_context
    def test_query_sql_injection(self):
        """Test API SQL Injection is not allowed works"""

        q = '1%3D1;SELECT%20*%20FROM%20task%20WHERE%201=1'
        res = self.app.get('/api/task?' + q)
        error = json.loads(res.data)
        assert res.status_code == 415, error
        assert error['action'] == 'GET', error
        assert error['status'] == 'failed', error
        assert error['target'] == 'task', error

        q = 'project_id=1%3D1;SELECT%20*%20FROM%20task%20WHERE%201'
        res = self.app.get('/api/apappp?' + q)
        assert res.status_code == 404, res.data

        q = 'project_id=1%3D1;SELECT%20*%20FROM%20task%20WHERE%201'
        res = self.app.get('/api/' + q)
        assert res.status_code == 404, res.data

        q = 'project_id=1%3D1;SELECT%20*%20FROM%20task%20WHERE%201'
        res = self.app.get('/api' + q)
        assert res.status_code == 404, res.data


    def test_jsonpify(self):
        """Test API jsonpify decorator works."""
        res = self.app.get('/api/project/1?callback=mycallback')
        err_msg = "mycallback should be included in the response"
        assert "mycallback" in res.data, err_msg
        err_msg = "Status code should be 200"
        assert res.status_code == 200, err_msg


    def test_cors(self):
        """Test CORS decorator works."""
        res = self.app.get('/api/project/1')
        err_msg = "CORS should be enabled"
        print res.headers
        assert res.headers['Access-Control-Allow-Origin'] == '*', err_msg
        methods = ['PUT', 'HEAD', 'DELETE', 'OPTIONS', 'GET']
        for m in methods:
            assert m in res.headers['Access-Control-Allow-Methods'], err_msg
        assert res.headers['Access-Control-Max-Age'] == '21600', err_msg
        headers = 'CONTENT-TYPE, AUTHORIZATION'
        assert res.headers['Access-Control-Allow-Headers'] == headers, err_msg
