"""
    binder
    ~~~~~~

    binder is a learning social network. It helps you find and learn with
    other students. Give it a whirl. Sign up today!

    binder is also open source software and available under the MIT license.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details

"""
import sys

if sys.version < '3.2.0':
    raise RuntimeError("You need at least python 3.4 for binder to work.")

from setuptools import setup


install_requires = [
    'Flask==0.10.1',
    'Flask-Bootstrap==3.3.5.6',
    'Flask-Menu==0.4.0',
    'Flask-Script==2.0.5',
    'Flask-SQLAlchemy==2.0',
    'SQLAlchemy==1.0.8',
    'Flask-Login==0.2.11',
    'rq==0.5.5',
    'Flask-Dance==0.7.0',
    'blinker==1.4',
]

if '3.2.0' < sys.version < '3.4.0':
    install_requires.append('enum34==1.0.4')

setup(
    name='binder',
    version='0.0.4',
    description='Brings students closer.',
    license='MIT',
    long_description=__doc__,
    packages=['binder', 'binder.pages'],
    author='Ananth Bhaskararaman',
    author_email='antsub@gmail.com',
    url='http://github.com/ananthb/binder',
    platforms='any',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'binder = binder:binder_app'
        ],
    },
    zip_safe=True,
)
