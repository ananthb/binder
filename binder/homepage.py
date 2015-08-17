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
