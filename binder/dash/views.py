"""
    binder.dashboard.views
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

from flask import Blueprint, render_template
from flask_menu import register_menu
from flask.ext.login import login_required

DashBoard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@DashBoard.route('/me')
@register_menu(DashBoard, '.dash', 'Dash')
@login_required
def me():
    return render_template('dash/me.html')
