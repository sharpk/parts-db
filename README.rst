Partridge
======

A basic electronic parts database.

This project is based on the Flaskr blog app built in the Flask `tutorial`_.

.. _tutorial: https://flask.palletsprojects.com/tutorial/


Install
-------

::

    # clone the repository
    $ git clone https://github.com/sharpk/parts-db
    $ cd parts-db

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Partridge::

    $ pip install -e .

Or if you are using the master branch, install Flask from source before
installing Partridge::

    $ pip install -e ../..
    $ pip install -e .


Run
---

::

    $ export FLASK_APP=partridge
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=partridge
    > set FLASK_ENV=development
    > flask init-db
    > flask run

Open http://127.0.0.1:5000 in a browser.

Import Database
---------------

Run the following command on a .sql file that has a format matching partridge/schema.sql

    > flask import-db <sql-file>

Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
