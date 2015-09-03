"""
    binder.dashboard.views
    ~~~~~~~~~~~~~~~~~~~~~~

"""

from flask import Blueprint, session, render_template
from flask_menu import register_menu

DashBoard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@DashBoard.route('/me')
@register_menu(DashBoard, '.dash', 'Dash')
def me():
    return render_template('dash/home.html')
