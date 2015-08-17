"""
    binder.homepage
    ~~~~~~~~~~~~~~~

    Blueprint to render the index template and display a homepage.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, See LICENSE for more details

"""

from flask import Blueprint
from flask import render_template

home = Blueprint(
    'home',
    __name__,
    template_folder='templates'
)


@home.route('/')
def show():
    return render_template('index.html')
