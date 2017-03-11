CookieEater
===========

|BuildStatus| |CoverageStatus|

**Browser Cookie Management**

Overview
--------

Firefox and Chrome Cookie management. (Chrome requires SQLite 3.8 or greater.)

Install
-------

.. code::

        pip install cookie-eater

CI tests run on:

* Python 2.6+
* Python 3.3+
* Pypy


Example Usage
~~~~~~~~~~~~~

.. code:: python

        import cookie_eater

        fox = cookie_eater.FirefoxCookies()
        # Automatically uses the DB of the default profile, can specify db=<path>

        fox.add_cookie("example.com", "MyCookie", "Cookie contents!")

        fox.find_cookies(host="Example")
        # [{'host': u'example.com', 'name': u'MyCookie', 'value': u'Cookie contents!'}]

        fox.delete_cookie("example.com", "MyCookie")




.. |CoverageStatus| image:: https://coveralls.io/repos/github/cdgriffith/CookieEater/badge.svg?branch=master
   :target: https://coveralls.io/github/cdgriffith/CookieEater?branch=master
.. |BuildStatus| image:: https://travis-ci.org/cdgriffith/Reusables.svg?branch=master
    :target: https://travis-ci.org/cdgriffith/Reusables
