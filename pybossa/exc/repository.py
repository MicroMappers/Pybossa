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


class DBIntegrityError(Exception):
    """Raised when an integrity exception in the DB layer occurs"""
    def __init__(self, message):
        super(DBIntegrityError, self).__init__(message)
        self.message = message


class WrongObjectError(Exception):
    """Raised when trying to save, update or delete objects that the repository
    does not handle"""
    def __init__(self, message):
        super(WrongObjectError, self).__init__(message)
        self.message = message