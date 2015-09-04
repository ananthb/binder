"""
    binder.pages.views
    ~~~~~~~~~~~~~~~

    Static pages are rendered here

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, See LICENSE for more details
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_menu import register_menu
from flask.ext.login import current_user

Pages = Blueprint(
    'pages',
    __name__,
)


@Pages.route('/')
@register_menu(Pages, '.home', 'Home', order=0)
def index():
    #if current_user.is_authenticated:
    #    return redirect(url_for('dashboard.me'))
    return render_template('pages/index.html')


@Pages.route('/contact')
@register_menu(Pages, '.contact', 'Contact', order=1)
def contact():
    return render_template('pages/contact.html')
