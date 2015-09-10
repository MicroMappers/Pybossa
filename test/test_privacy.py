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

from bs4 import BeautifulSoup

from helper import web as web_helper
from default import flask_app, with_context
from mock import patch


class TestPrivacyWebPublic(web_helper.Helper):

    def setUp(self):
        super(TestPrivacyWebPublic, self).setUp()
        with self.flask_app.app_context():
            self.create()

    # Tests
    @with_context
    def test_00_footer(self):
        """Test PRIVACY footer privacy is respected"""
        url = '/'
        # As Anonymou user
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Footer links should be shown to anonymous users"
        assert dom.find(id='footer_links') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Footer links should be shown to authenticated users"
        assert dom.find(id='footer_links') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Footer links should be shown to admin users"
        assert dom.find(id='footer_links') is not None, err_msg
        self.signout()

    @with_context
    def test_01_front_page(self):
        """Test PRIVACY footer privacy is respected"""
        url = '/'
        # As Anonymou user
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Top users should be shown to anonymous users"
        assert dom.find(id='top_users') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Top users should be shown to authenticated users"
        assert dom.find(id='top_users') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Top users should be shown to admin"
        assert dom.find(id='top_users') is not None, err_msg
        self.signout()

    @with_context
    def test_02_account_index(self):
        """Test PRIVACY account privacy is respected"""
        # As Anonymou user
        url = "/account"
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Community page should be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Community page should be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Community page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @with_context
    def test_03_leaderboard(self):
        """Test PRIVACY leaderboard privacy is respected"""
        # As Anonymou user
        url = "/leaderboard"
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Leaderboard page should be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Leaderboard page should be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Leaderboard page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @with_context
    def test_04_global_stats_index(self):
        """Test PRIVACY global stats privacy is respected"""
        # As Anonymou user
        url = "/stats"
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Stats page should be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Stats page should be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Stats page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @with_context
    def test_05_app_stats_index(self):
        """Test PRIVACY project stats privacy is respected"""
        # As Anonymou user
        url = "/project/%s/stats" % self.project_short_name
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Project Stats page should be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Project Stats page should be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Project Stats page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @with_context
    def test_06_user_public_profile(self):
        """Test PRIVACY user public profile privacy is respected"""
        # As Anonymou user
        url = "/account/%s" % self.name
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Public User Profile page should be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Public User Profile page should be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Public User Profile page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()


class TestPrivacyWebPrivacy(web_helper.Helper):

    def setUp(self):
        super(TestPrivacyWebPrivacy, self).setUp()
        with self.flask_app.app_context():
            self.create()

    # Tests
    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_00_footer(self):
        """Test PRIVACY footer privacy is respected"""
        url = '/'
        # As Anonymou user
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Footer links should not be shown to anonymous users"
        assert dom.find(id='footer_links') is None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Footer links should not be shown to authenticated users"
        assert dom.find(id='footer_links') is None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Footer links should not be shown to admin users"
        assert dom.find(id='footer_links') is None, err_msg
        self.signout()

    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_01_front_page(self):
         """Test PRIVACY front page top users privacy is respected"""
         url = '/'
         # As Anonymou user
         res = self.app.get(url, follow_redirects=True)
         dom = BeautifulSoup(res.data)
         err_msg = "Top users should not be shown to anonymous users"
         assert dom.find(id='top_users') is None, err_msg
         # As Authenticated user but NOT ADMIN
         self.signin()
         res = self.app.get(url, follow_redirects=True)
         dom = BeautifulSoup(res.data)
         err_msg = "Top users should not be shown to authenticated users"
         assert dom.find(id='top_users') is None, err_msg
         self.signout
         # As Authenticated user but ADMIN
         res = self.signin(email=self.root_addr, password=self.root_password)
         print res.data
         res = self.app.get(url, follow_redirects=True)
         dom = BeautifulSoup(res.data)
         err_msg = "Top users should be shown to admin"
         assert dom.find(id='top_users') is not None, err_msg
         self.signout()

    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_02_account_index(self):
        """Test PRIVACY account privacy is respected"""
        # As Anonymou user
        url = "/account"
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Community page should not be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Community page should not be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Community page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_03_leaderboard(self):
        """Test PRIVACY leaderboard privacy is respected"""
        # As Anonymou user
        url = "/leaderboard"
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Leaderboard page should not be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Leaderboard page should not be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Leaderboard page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_04_global_stats_index(self):
        """Test PRIVACY global stats privacy is respected"""
        # As Anonymou user
        url = "/stats"
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Stats page should not be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Stats page should not be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Stats page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_05_app_stats_index(self):
        """Test PRIVACY project stats privacy is respected"""
        # As Anonymou user
        url = "/project/%s/stats" % self.project_short_name
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Project Stats page should not be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Project Stats page should not be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Project Stats page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()

    @patch.dict(flask_app.config, {'ENFORCE_PRIVACY': True})
    @with_context
    def test_06_user_public_profile(self):
        """Test PRIVACY user public profile privacy is respected"""
        # As Anonymou user
        url = "/account/%s" % self.name
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Public User Profile page should not be shown to anonymous users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        # As Authenticated user but NOT ADMIN
        self.signin()
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Public User Profile page should not be shown to authenticated users"
        assert dom.find(id='enforce_privacy') is not None, err_msg
        self.signout
        # As Authenticated user but ADMIN
        self.signin(email=self.root_addr, password=self.root_password)
        res = self.app.get(url, follow_redirects=True)
        dom = BeautifulSoup(res.data)
        err_msg = "Public User Profile page should be shown to admin users"
        assert dom.find(id='enforce_privacy') is None, err_msg
        self.signout()
