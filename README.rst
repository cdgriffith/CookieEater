CookieEater
===========

**Browser Cookie Management**

Overview
~~~~~~~~

Firefox and Chrome Cookie management. (Chrome requires SQLite 3.8 or greater.)


.. code:: python

        import cookie_eater

        fox = cookie_eater.FirefoxCookies()
        # Automatically uses the DB of the default profile, can specify db=<path>

        fox.add_cookie("example.com", "MyCookie", "Cookie contents!")

        fox.find_cookies(host="Example")
        # [{'host': u'example.com', 'name': u'MyCookie', 'value': u'Cookie contents!'}]

        fox.delete_cookie("example.com", "MyCookie")


