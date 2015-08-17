"""
binder
~~~~~~

binder is a learning social network. It helps you find and learn with
other students. Give it a whirl. Sign up today!

binder is also open source software and available under the MIT license.


"""

from setuptools import setup

setup(
    name='binder',
    version='0.0.1',
    description='Brings students closer.',
    license='MIT',
    long_description=__doc__,
    packages=['binder'],
    author='Ananth Bhaskararaman',
    author_email='antsub@gmail.com',
    platforms='any',
    install_requires=[
        'flask>=0.10',
        'flask-script>=2.0.5'
    ],
    entry_points={
        'console_scripts': [
            'binder = binder:cmdline'
        ],
    },
    zip_safe=True,
)
