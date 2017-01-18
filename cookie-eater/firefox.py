#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Part of the CookieEater package.
#
# Copyright (c) 2017 - Chris Griffith - MIT License
import os

from .base import *

__all__ = ['FirefoxCookiesV1', 'FirefoxCookies']


class FirefoxCookiesV1(CookieManager):
    """First iteration of Firefox Cookie manager, developed with Firefox 48.

    Custom add_cookie kwargs:

    * base_domain: str
    * origin_attributes: str
    * app_id: int
    * in_browser_element: bool

    """
    _valid_structure = {"tables": [("moz_cookies",)],
                        "columns": ['id', 'baseDomain', 'originAttributes',
                                    'name', 'value', 'host', 'path', 'expiry',
                                    'lastAccessed', 'creationTime', 'isSecure',
                                    'isHttpOnly', 'appId', 'inBrowserElement']}

    _insert = ("INSERT INTO moz_cookies (baseDomain, originAttributes,"
               " name, value, host, path, expiry, lastAccessed, "
               "creationTime, isSecure, isHttpOnly, appId, inBrowserElement"
               ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

    _db_paths = {
        "windows": "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\",
        "mac": "~/Library/Application Support/Firefox/Profiles/",
        "linux": "~/.mozilla/firefox/"}
    table_name = "moz_cookies"

    @staticmethod
    def _find_db_extra(expanded_path):
        """Firefox profiles path has a folder that ends with .default that
        must be found."""
        default = [x for x in os.listdir(expanded_path)
                   if x.endswith(".default")]
        if not default:
            raise MissingCookiesDB("No default profile in "
                                   "{0}".format(expanded_path))
        return os.path.join(expanded_path, default[0], "cookies.sqlite")

    def _insert_command(self, cursor, host, name, value, path,
                        expires_in, secure, http_only, **kwargs):
        """Firefox specific SQL insert command with required times"""
        now = self._current_time(length=16)
        exp = self._expire_time(length=10, expires_in=expires_in)
        base_domain = str(kwargs.get("base_domain", ".".join(host.split(".")
                          [-2 if not host.endswith(".co.uk") else -3:])))

        return cursor.execute(self._insert, (base_domain,
                              str(kwargs.get('origin_attributes', "")),
                              name, value, host, path, exp, now, now,
                              secure, http_only,
                              int(kwargs.get('app_id', 0)),
                              int(bool(kwargs.get('in_browser_element', 0)))))

    def _delete_command(self, cursor, host, name):
        """Firefox specific SQL delete command"""
        return cursor.execute("DELETE FROM moz_cookies WHERE host=? AND name=?",
                              (host, name))

    def _limited_select_command(self, cursor):
        """Firefox specific SQL select command"""
        return cursor.execute("SELECT rowid, host, name, value FROM "
                              "moz_cookies")

    def _match_command(self, cursor, match, value):
        """Firefox specific SQL select command with matching"""
        return cursor.execute("SELECT * FROM "
                              "moz_cookies WHERE {0}=?".format(match), (value,))

    def _row_to_dict(self, row):
        """Returns a SQL query row as a standard dictionary."""
        return {"host": row[5], "name": row[3], "value": row[4],
                "created": self._int_time_to_float(row[9]),
                "expires": self._int_time_to_float(row[7])}


class FirefoxCookies(FirefoxCookiesV1):
    """Current version of Firefox cookie management"""
