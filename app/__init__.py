#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Start web server

Keyword arguments: none
argument -- description
Return: object -> web server starting
"""

from .server import server
from .config import Dev
from .server.helpers.web.routes import users, notes

app = server(Dev, users, notes)


if __name__ == '__main__':
    app.run()