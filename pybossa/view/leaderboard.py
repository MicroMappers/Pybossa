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
"""Leaderboard view for PyBossa."""
from flask import Blueprint, current_app
from flask import render_template
from flask.ext.login import current_user
from pybossa.cache import users as cached_users

blueprint = Blueprint('leaderboard', __name__)


@blueprint.route('/')
def index():
    """Get the last activity from users and projects."""
    if current_user.is_authenticated():
        user_id = current_user.id
    else:
        user_id = None
    top_users = cached_users.get_leaderboard(current_app.config['LEADERBOARD'],
                                             user_id=user_id)

    return render_template('/stats/index.html', title="Community Leaderboard",
                           top_users=top_users)
