#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Part of the CookieEater package.
#
# Copyright (c) 2017 - Chris Griffith - MIT License
import datetime
import sqlite3

from .base import *

__all__ = ['ChromeCookiesV1', 'ChromeCookies']


class ChromeCookiesV1(CookieManager):
    """First iteration of Chrome Cookie manager. Developed with Chrome 52.

    Custom add_cookie kwargs:

    * has_expires: bool
    * persistent: bool
    * priority: bool
    * encrypted_value: str
    * first_party_only: bool

    """
    _valid_structure = {"tables": [("meta",), ("cookies",)],
                        "columns": ['creation_utc', 'host_key', 'name', 'value',
                                    'path', 'expires_utc', 'secure', 'httponly',
                                    'last_access_utc', 'has_expires',
                                    'persistent', 'priority', 'encrypted_value',
                                    'firstpartyonly']}
    _db_paths = {
        "windows": "~\\AppData\\Local\\Google\\Chrome"
                   "\\User Data\\Default\\Cookies",
        "mac": "~/Library/Application Support/Google/Chrome/Default/Cookies",
        "linux": "~/.config/google-chrome/Default/Cookies"}
    _insert = ("INSERT INTO cookies (creation_utc, host_key, name, value, "
               "path, expires_utc, secure, httponly, last_access_utc, "
               "has_expires, persistent, priority, encrypted_value,"
               " firstpartyonly) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
               "?, ?, ?, ?, ?, ?)")
    table_name = "cookies"

    def __init__(self, db=None):
        major, minor = sqlite3.sqlite_version.split(".")[:2]
        if int(major) < 3 or (int(major) == 3 and int(minor) < 8):
            raise BrowserException("SQLite 3.8 or higher required for chrome"
                                   "- {0}.{1} installed".format(major, minor))
        super(ChromeCookiesV1, self).__init__(db)

    def _insert_command(self, cursor, host, name, value, path,
                        expires_in, secure, http_only, **kwargs):
        """Chrome specific SQL insert command with required times"""
        now = self._current_time(epoch=datetime.datetime(1601, 1, 1), length=17)
        exp = self._expire_time(epoch=datetime.datetime(1601, 1, 1), length=17,
                                expires_in=expires_in)

        return cursor.execute(self._insert, (now, host, name, value, path,
                              exp, secure, http_only, now,
                              int(bool(kwargs.get('has_expires', 1))),
                              int(bool(kwargs.get('persistent', 1))),
                              int(kwargs.get('priority', 1)),
                              str(kwargs.get('encrypted_value', "")),
                              int(bool(kwargs.get('first_party_only', 0)))))

    def _int_time_to_float(self, int_time, period_placement=10):
        """Chrome has a stupid different epoch of 1601, 1 ,1"""
        offset_time = (int_time -
                       int(str(11644473600).ljust(len(str(int_time)), "0")))
        return super(ChromeCookiesV1, self)._int_time_to_float(
            int_time=offset_time, period_placement=period_placement)

    def _delete_command(self, cursor, host, name):
        """Chrome specific SQL delete command"""
        return cursor.execute("DELETE FROM cookies WHERE host_key=? AND name=?",
                              (host, name))

    def _limited_select_command(self, cursor):
        """Chrome specific SQL select command"""
        return cursor.execute("SELECT rowid, host_key, name, value FROM "
                              "cookies")

    def _match_command(self, cursor, match, value):
        """Chrome specific SQL select command with matching"""
        return cursor.execute("SELECT * FROM "
                              "cookies WHERE {0}=?".format(match), (value,))

    def _row_to_dict(self, row):
        """Returns a SQL query row as a standard dictionary"""
        return {"host": row[1], "name": row[2], "value": row[3],
                "created": self._int_time_to_float(row[0]),
                "expires": 0 if not row[9] else self._int_time_to_float(row[5])}


class ChromeCookies(ChromeCookiesV1):
    """Current version of Chrome cookie management"""
