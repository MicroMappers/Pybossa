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

# DEBUG = False

## webserver host and port
# HOST = '0.0.0.0'
# PORT = 5000

SECRET = 'foobar'
SECRET_KEY = 'my-session-secret'

SQLALCHEMY_DATABASE_URI = 'postgresql://pybossa:tester@localhost/pybossa'

##Slave configuration for DB
#SQLALCHEMY_BINDS = {
#    'slave': 'postgresql://user:password@server/db'
#}

ITSDANGEROUSKEY = 'its-dangerous-key'

## project configuration
BRAND = 'PyBossa'
TITLE = 'PyBossa'
LOGO = 'default_logo.png'
COPYRIGHT = 'Set Your Institution'
DESCRIPTION = 'Set the description in your config'
TERMSOFUSE = 'http://okfn.org/terms-of-use/'
DATAUSE = 'http://opendatacommons.org/licenses/by/'
CONTACT_EMAIL = 'info@pybossa.com'
CONTACT_TWITTER = 'PyBossa'

## Default number of projects per page
## APPS_PER_PAGE = 20

## External Auth providers
# TWITTER_CONSUMER_KEY=''
# TWITTER_CONSUMER_SECRET=''
# FACEBOOK_APP_ID=''
# FACEBOOK_APP_SECRET=''
# GOOGLE_CLIENT_ID=''
# GOOGLE_CLIENT_SECRET=''

## Supported Languages
## NOTE: You need to create a symbolic link to the translations folder, otherwise
## this wont work.
## ln -s pybossa/themes/your-theme/translations pybossa/translations
#DEFAULT_LOCALE = 'en'
#LOCALES = [('en', 'English'), ('es', u'Español'),
#           ('it', 'Italiano'), ('fr', u'Français'),
#           ('ja', u'日本語')]


## list of administrator emails to which error emails get sent
# ADMINS = ['me@sysadmin.org']

## CKAN URL for API calls
#CKAN_NAME = "Demo CKAN server"
#CKAN_URL = "http://demo.ckan.org"


## logging config
# Sentry configuration
# SENTRY_DSN=''
## set path to enable
# LOG_FILE = '/path/to/log/file'
## Optional log level
# import logging
# LOG_LEVEL = logging.DEBUG

## Mail setup
MAIL_SERVER = 'localhost'
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_PORT = 25
MAIL_FAIL_SILENTLY = False
MAIL_DEFAULT_SENDER = 'PyBossa Support <info@pybossa.com>'

## Announcement messages
## Use any combination of the next type of messages: root, user, and app owners
## ANNOUNCEMENT = {'admin': 'Root Message', 'user': 'User Message', 'owner': 'Owner Message'}

## Enforce Privacy Mode, by default is disabled
## This config variable will disable all related user pages except for admins
## Stats, top users, leaderboard, etc
ENFORCE_PRIVACY = False


## Cache setup. By default it is enabled
## Redis Sentinel
# List of Sentinel servers (IP, port)
REDIS_CACHE_ENABLED = True
REDIS_SENTINEL = [('localhost', 26379)]
REDIS_MASTER = 'mymaster'
REDIS_DB = 0
REDIS_KEYPREFIX = 'pybossa_cache'

## Allowed upload extensions
ALLOWED_EXTENSIONS = ['js', 'css', 'png', 'jpg', 'jpeg', 'gif', 'zip']

## If you want to use the local uploader configure which folder
UPLOAD_METHOD = 'local'
UPLOAD_FOLDER = 'uploads'

## If you want to use Rackspace for uploads, configure it here
# RACKSPACE_USERNAME = 'username'
# RACKSPACE_API_KEY = 'apikey'
# RACKSPACE_REGION = 'ORD'

## Default number of users shown in the leaderboard
# LEADERBOARD = 20
## Default shown presenters
# PRESENTERS = ["basic", "image", "sound", "video", "map", "pdf"]
# Default Google Docs spreadsheet template tasks URLs
TEMPLATE_TASKS = {
    'image': "https://docs.google.com/spreadsheet/ccc?key=0AsNlt0WgPAHwdHFEN29mZUF0czJWMUhIejF6dWZXdkE&usp=sharing",
    'sound': "https://docs.google.com/spreadsheet/ccc?key=0AsNlt0WgPAHwdEczcWduOXRUb1JUc1VGMmJtc2xXaXc&usp=sharing",
    'video': "https://docs.google.com/spreadsheet/ccc?key=0AsNlt0WgPAHwdGZ2UGhxSTJjQl9YNVhfUVhGRUdoRWc&usp=sharing",
    'map': "https://docs.google.com/spreadsheet/ccc?key=0AsNlt0WgPAHwdGZnbjdwcnhKRVNlN1dGXy0tTnNWWXc&usp=sharing",
    'pdf': "https://docs.google.com/spreadsheet/ccc?key=0AsNlt0WgPAHwdEVVamc0R0hrcjlGdXRaUXlqRXlJMEE&usp=sharing"}

# Expiration time for password protected project cookies
PASSWD_COOKIE_TIMEOUT = 60 * 30

# Expiration time for account confirmation / password recovery links
ACCOUNT_LINK_EXPIRATION = 5 * 60 * 60

## Ratelimit configuration
# LIMIT = 300
# PER = 15 * 60

# Disable new account confirmation (via email)
ACCOUNT_CONFIRMATION_DISABLED = True

# Mailchimp API key
# MAILCHIMP_API_KEY = "your-key"
# MAILCHIMP_LIST_ID = "your-list-ID"

# Flickr API key and secret
# FLICKR_API_KEY = 'your-key'
# FLICKR_SHARED_SECRET = 'your-secret'

# DROPBOX APP KEY
# DROPBOX_APP_KEY = 'your-key'

# Send emails weekly update every
# WEEKLY_UPDATE_STATS = 'Sunday'
