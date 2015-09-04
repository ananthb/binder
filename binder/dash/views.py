"""
    binder.dashboard.views
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

from flask import Blueprint, render_template, flash
from flask_menu import register_menu
from flask.ext.login import current_user, login_required

DashBoard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@DashBoard.route('/me')
@register_menu(DashBoard, '.dash', 'Dash')
@login_required
def me():
    flash("Hi there, {}".format(current_user.Name))
    return render_template('dash/me.html')
