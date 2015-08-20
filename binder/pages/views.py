"""
    binder.pages.homepage
    ~~~~~~~~~~~~~~~

    Blueprint to render the index template and display a homepage.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, See LICENSE for more details

"""

from flask import Blueprint
from flask import render_template
from flask_menu import register_menu

Pages = Blueprint(
    'pages',
    __name__,
)


@Pages.route('/')
@register_menu(Pages, '.home', 'Home', order=0)
def index():
    return render_template('pages/index.html')


@Pages.route('/contact')
@register_menu(Pages, '.contact', 'Contact', order=1)
def contact():
    return render_template('pages/contact.html')
