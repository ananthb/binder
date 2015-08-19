"""
    binder.pages.homepage
    ~~~~~~~~~~~~~~~

    Blueprint to render the index template and display a homepage.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, See LICENSE for more details

"""

from flask import Blueprint
from flask import render_template


Pages = Blueprint(
    'pages',
    __name__,
    static_folder='static',
    template_folder='templates',
)

@Pages.route('/')
def index():
    return render_template('pages/index.html')
