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
from nose.tools import assert_equal
from test_api import TestAPI
from mock import patch
from factories import (ProjectFactory, TaskFactory, TaskRunFactory,
                        AnonymousTaskRunFactory, UserFactory)



class TestTaskrunAPI(TestAPI):


    @with_context
    def test_taskrun_query_without_params(self):
        """Test API TaskRun query"""
        TaskRunFactory.create_batch(10, info={'answer': 'annakarenina'})
        res = self.app.get('/api/taskrun')
        taskruns = json.loads(res.data)
        assert len(taskruns) == 10, taskruns
        taskrun = taskruns[0]
        assert taskrun['info']['answer'] == 'annakarenina', taskrun

        # The output should have a mime-type: application/json
        assert res.mimetype == 'application/json', res


    @with_context
    def test_query_taskrun(self):
        """Test API query for taskrun with params works"""
        project = ProjectFactory.create()
        task_runs = TaskRunFactory.create_batch(10, project=project)
        # Test for real field
        res = self.app.get("/api/taskrun?project_id=1")
        data = json.loads(res.data)
        # Should return one result
        assert len(data) == 10, data
        # Correct result
        assert data[0]['project_id'] == 1, data

        # Valid field but wrong value
        res = self.app.get("/api/taskrun?project_id=99999999")
        data = json.loads(res.data)
        assert len(data) == 0, data

        # Multiple fields
        res = self.app.get('/api/taskrun?project_id=1&task_id=1')
        data = json.loads(res.data)
        # One result
        assert len(data) == 1, data
        # Correct result
        assert data[0]['project_id'] == 1, data
        assert data[0]['task_id'] == 1, data

        # Limits
        res = self.app.get("/api/taskrun?project_id=1&limit=5")
        data = json.loads(res.data)
        for item in data:
            assert item['project_id'] == 1, item
        assert len(data) == 5, data

        # Keyset pagination
        url = "/api/taskrun?project_id=1&limit=5&last_id=%s" % task_runs[4].id
        res = self.app.get(url)
        data = json.loads(res.data)
        for item in data:
            assert item['project_id'] == 1, item
        assert len(data) == 5, data
        assert data[0]['id'] == task_runs[5].id, data[0]['id']


    @with_context
    @patch('pybossa.api.task_run.request')
    @patch('pybossa.api.task_run._check_task_requested_by_user')
    def test_taskrun_anonymous_post(self, fake_validation, mock_request):
        """Test API TaskRun creation and auth for anonymous users"""
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project)
        data = dict(
            project_id=project.id,
            task_id=task.id,
            info='my task result')

        # With wrong project_id
        mock_request.remote_addr = '127.0.0.0'
        data['project_id'] = 100000000000000000
        datajson = json.dumps(data)
        tmp = self.app.post('/api/taskrun', data=datajson)
        err_msg = "This post should fail as the project_id is wrong"
        err = json.loads(tmp.data)
        assert tmp.status_code == 403, tmp.data
        assert err['status'] == 'failed', err_msg
        assert err['status_code'] == 403, err_msg
        assert err['exception_msg'] == 'Invalid project_id', err_msg
        assert err['exception_cls'] == 'Forbidden', err_msg
        assert err['target'] == 'taskrun', err_msg

        # With wrong task_id
        data['project_id'] = task.project_id
        data['task_id'] = 100000000000000000000
        datajson = json.dumps(data)
        tmp = self.app.post('/api/taskrun', data=datajson)
        err = json.loads(tmp.data)
        assert tmp.status_code == 403, err_msg
        assert err['status'] == 'failed', err_msg
        assert err['status_code'] == 403, err_msg
        assert err['exception_msg'] == 'Invalid task_id', err_msg
        assert err['exception_cls'] == 'Forbidden', err_msg
        assert err['target'] == 'taskrun', err_msg

        # Now with everything fine
        data = dict(
            project_id=task.project_id,
            task_id=task.id,
            info='my task result')
        datajson = json.dumps(data)
        tmp = self.app.post('/api/taskrun', data=datajson)
        r_taskrun = json.loads(tmp.data)
        assert tmp.status_code == 200, r_taskrun

        # If the anonymous tries again it should be forbidden
        tmp = self.app.post('/api/taskrun', data=datajson)
        err_msg = ("Anonymous users should be only allowed to post \
                    one task_run per task")
        assert tmp.status_code == 403, err_msg

    @with_context
    @patch('pybossa.api.task_run._check_task_requested_by_user')
    def test_taskrun_authenticated_post(self, fake_validation):
        """Test API TaskRun creation and auth for authenticated users"""
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project)
        data = dict(
            project_id=project.id,
            task_id=task.id,
            info='my task result')

        # With wrong project_id
        data['project_id'] = 100000000000000000
        datajson = json.dumps(data)
        url = '/api/taskrun?api_key=%s' % project.owner.api_key
        tmp = self.app.post(url, data=datajson)
        err_msg = "This post should fail as the project_id is wrong"
        err = json.loads(tmp.data)
        assert tmp.status_code == 403, err_msg
        assert err['status'] == 'failed', err_msg
        assert err['status_code'] == 403, err_msg
        assert err['exception_msg'] == 'Invalid project_id', err_msg
        assert err['exception_cls'] == 'Forbidden', err_msg
        assert err['target'] == 'taskrun', err_msg

        # With wrong task_id
        data['project_id'] = task.project_id
        data['task_id'] = 100000000000000000000
        datajson = json.dumps(data)
        tmp = self.app.post(url, data=datajson)
        err_msg = "This post should fail as the task_id is wrong"
        err = json.loads(tmp.data)
        assert tmp.status_code == 403, err_msg
        assert err['status'] == 'failed', err_msg
        assert err['status_code'] == 403, err_msg
        assert err['exception_msg'] == 'Invalid task_id', err_msg
        assert err['exception_cls'] == 'Forbidden', err_msg
        assert err['target'] == 'taskrun', err_msg

        # Now with everything fine
        data = dict(
            project_id=task.project_id,
            task_id=task.id,
            user_id=project.owner.id,
            info='my task result')
        datajson = json.dumps(data)
        tmp = self.app.post(url, data=datajson)
        r_taskrun = json.loads(tmp.data)
        assert tmp.status_code == 200, r_taskrun

        # If the user tries again it should be forbidden
        tmp = self.app.post(url, data=datajson)
        assert tmp.status_code == 403, tmp.data


    def test_taskrun_post_requires_newtask_first_anonymous(self):
        """Test API TaskRun post fails if task was not previously requested for
        anonymous user"""
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project)
        data = dict(
            project_id=project.id,
            task_id=task.id,
            info='my task result')
        datajson = json.dumps(data)
        fail = self.app.post('/api/taskrun', data=datajson)
        err = json.loads(fail.data)

        assert fail.status_code == 403, fail.status_code
        assert err['status'] == 'failed', err
        assert err['status_code'] == 403, err
        assert err['exception_msg'] == 'You must request a task first!', err
        assert err['exception_cls'] == 'Forbidden', err
        assert err['target'] == 'taskrun', err

        # Succeeds after requesting a task
        self.app.get('/api/project/%s/newtask' % project.id)
        success = self.app.post('/api/taskrun', data=datajson)
        assert success.status_code == 200, success.data


    @with_context
    def test_taskrun_post_requires_newtask_first_authenticated(self):
        """Test API TaskRun post fails if task was not previously requested for
        authenticated user"""
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project)
        data = dict(
            project_id=project.id,
            task_id=task.id,
            info='my task result')
        datajson = json.dumps(data)
        url = '/api/taskrun?api_key=%s' % project.owner.api_key
        fail = self.app.post(url, data=datajson)
        err = json.loads(fail.data)

        assert fail.status_code == 403, fail.status_code
        assert err['status'] == 'failed', err
        assert err['status_code'] == 403, err
        assert err['exception_msg'] == 'You must request a task first!', err
        assert err['exception_cls'] == 'Forbidden', err
        assert err['target'] == 'taskrun', err

        # Succeeds after requesting a task
        self.app.get('/api/project/%s/newtask?api_key=%s' % (project.id, project.owner.api_key))
        success = self.app.post(url, data=datajson)
        assert success.status_code == 200, success.data


    @with_context
    def test_taskrun_post_with_bad_data(self):
        """Test API TaskRun error messages."""
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project)
        project_id = project.id
        task_run = dict(project_id=project.id, task_id=task.id, info='my task result')
        url = '/api/taskrun?api_key=%s' % project.owner.api_key

        # POST with not JSON data
        res = self.app.post(url, data=task_run)
        err = json.loads(res.data)
        assert res.status_code == 415, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'POST', err
        assert err['exception_cls'] == 'ValueError', err

        # POST with not allowed args
        res = self.app.post(url + '&foo=bar', data=task_run)
        err = json.loads(res.data)
        assert res.status_code == 415, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'POST', err
        assert err['exception_cls'] == 'AttributeError', err

        # POST with fake data
        task_run['wrongfield'] = 13
        res = self.app.post(url, data=json.dumps(task_run))
        err = json.loads(res.data)
        assert res.status_code == 415, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'POST', err
        assert err['exception_cls'] == 'TypeError', err


    @with_context
    def test_taskrun_update(self):
        """Test TaskRun API update works"""
        admin = UserFactory.create()
        owner = UserFactory.create()
        non_owner = UserFactory.create()
        project = ProjectFactory.create(owner=owner)
        task = TaskFactory.create(project=project)
        anonymous_taskrun = AnonymousTaskRunFactory.create(task=task, info='my task result')
        user_taskrun = TaskRunFactory.create(task=task, user=owner, info='my task result')

        task_run = dict(project_id=project.id, task_id=task.id, info='another result')
        datajson = json.dumps(task_run)

        # anonymous user
        # No one can update anonymous TaskRuns
        url = '/api/taskrun/%s' % anonymous_taskrun.id
        res = self.app.put(url, data=datajson)
        assert anonymous_taskrun, anonymous_taskrun
        assert_equal(anonymous_taskrun.user, None)
        error_msg = 'Should not be allowed to update'
        assert_equal(res.status, '401 UNAUTHORIZED', error_msg)

        # real user but not allowed as not owner!
        url = '/api/taskrun/%s?api_key=%s' % (user_taskrun.id, non_owner.api_key)
        res = self.app.put(url, data=datajson)
        error_msg = 'Should not be able to update TaskRuns of others'
        assert_equal(res.status, '403 FORBIDDEN', error_msg)

        # real user
        url = '/api/taskrun/%s?api_key=%s' % (user_taskrun.id, owner.api_key)
        out = self.app.get(url, follow_redirects=True)
        task = json.loads(out.data)
        datajson = json.loads(datajson)
        datajson['link'] = task['link']
        datajson['links'] = task['links']
        datajson = json.dumps(datajson)
        url = '/api/taskrun/%s?api_key=%s' % (user_taskrun.id, owner.api_key)
        res = self.app.put(url, data=datajson)
        out = json.loads(res.data)
        assert_equal(res.status, '403 FORBIDDEN', res.data)

        # PUT with not JSON data
        res = self.app.put(url, data=task_run)
        err = json.loads(res.data)
        assert res.status_code == 403, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'PUT', err
        assert err['exception_cls'] == 'Forbidden', err

        # PUT with not allowed args
        res = self.app.put(url + "&foo=bar", data=json.dumps(task_run))
        err = json.loads(res.data)
        assert res.status_code == 415, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'PUT', err
        assert err['exception_cls'] == 'AttributeError', err

        # PUT with fake data
        task_run['wrongfield'] = 13
        res = self.app.put(url, data=json.dumps(task_run))
        err = json.loads(res.data)
        assert res.status_code == 403, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'PUT', err
        assert err['exception_cls'] == 'Forbidden', err
        task_run.pop('wrongfield')

        # root user
        url = '/api/taskrun/%s?api_key=%s' % (user_taskrun.id, admin.api_key)
        res = self.app.put(url, data=datajson)
        assert_equal(res.status, '403 FORBIDDEN', res.data)


    @with_context
    def test_taskrun_delete(self):
        """Test TaskRun API delete works"""
        admin = UserFactory.create()
        owner = UserFactory.create()
        non_owner = UserFactory.create()
        project = ProjectFactory.create(owner=owner)
        task = TaskFactory.create(project=project)
        anonymous_taskrun = AnonymousTaskRunFactory.create(task=task, info='my task result')
        user_taskrun = TaskRunFactory.create(task=task, user=owner, info='my task result')

        ## anonymous
        res = self.app.delete('/api/taskrun/%s' % user_taskrun.id)
        error_msg = 'Anonymous should not be allowed to delete'
        assert_equal(res.status, '401 UNAUTHORIZED', error_msg)

        ### real user but not allowed to delete anonymous TaskRuns
        url = '/api/taskrun/%s?api_key=%s' % (anonymous_taskrun.id, owner.api_key)
        res = self.app.delete(url)
        error_msg = 'Authenticated user should not be allowed ' \
                    'to delete anonymous TaskRuns'
        assert_equal(res.status, '403 FORBIDDEN', error_msg)

        ### real user but not allowed as not owner!
        url = '/api/taskrun/%s?api_key=%s' % (user_taskrun.id, non_owner.api_key)
        res = self.app.delete(url)
        error_msg = 'Should not be able to delete TaskRuns of others'
        assert_equal(res.status, '403 FORBIDDEN', error_msg)

        #### real user
        # DELETE with not allowed args
        url = '/api/taskrun/%s?api_key=%s' % (user_taskrun.id, owner.api_key)
        res = self.app.delete(url + "&foo=bar")
        err = json.loads(res.data)
        assert res.status_code == 415, err
        assert err['status'] == 'failed', err
        assert err['target'] == 'taskrun', err
        assert err['action'] == 'DELETE', err
        assert err['exception_cls'] == 'AttributeError', err

        # Owner with valid args can delete
        res = self.app.delete(url)
        assert_equal(res.status, '204 NO CONTENT', res.data)

        ### root
        url = '/api/taskrun/%s?api_key=%s' % (anonymous_taskrun.id, admin.api_key)
        res = self.app.delete(url)
        error_msg = 'Admin should be able to delete TaskRuns of others'
        assert_equal(res.status, '204 NO CONTENT', error_msg)


    @with_context
    @patch('pybossa.api.task_run.request')
    @patch('pybossa.api.task_run._check_task_requested_by_user')
    def test_taskrun_updates_task_state(self, fake_validation, mock_request):
        """Test API TaskRun POST updates task state"""
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project, n_answers=2)
        url = '/api/taskrun?api_key=%s' % project.owner.api_key

        # Post first taskrun
        data = dict(
            project_id=task.project_id,
            task_id=task.id,
            user_id=project.owner.id,
            info='my task result')
        datajson = json.dumps(data)
        tmp = self.app.post(url, data=datajson)
        r_taskrun = json.loads(tmp.data)

        assert tmp.status_code == 200, r_taskrun

        err_msg = "Task state should be different from completed"
        assert task.state == 'ongoing', err_msg

        # Post second taskrun
        mock_request.remote_addr = '127.0.0.0'
        url = '/api/taskrun'
        data = dict(
            project_id=task.project_id,
            task_id=task.id,
            info='my task result anon')
        datajson = json.dumps(data)
        tmp = self.app.post(url, data=datajson)
        r_taskrun = json.loads(tmp.data)

        assert tmp.status_code == 200, r_taskrun
        err_msg = "Task state should be equal to completed"
        assert task.state == 'completed', err_msg

    @patch('pybossa.api.task_run._check_task_requested_by_user')
    def test_taskrun_create_with_reserved_fields_returns_error(self, requested):
        requested.return_value = True
        project = ProjectFactory.create()
        task = TaskFactory.create(project=project)
        url = '/api/taskrun?api_key=%s' % project.owner.api_key
        data = dict(
            project_id=task.project_id,
            task_id=task.id,
            user_id=project.owner.id,
            created='today',
            finish_time='now',
            id=222)
        datajson = json.dumps(data)

        resp = self.app.post(url, data=datajson)

        assert resp.status_code == 400, resp.status_code
        error = json.loads(resp.data)
        assert error['exception_msg'] == "Reserved keys in payload", error
