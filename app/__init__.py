#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Start web server

Keyword arguments: none
argument -- description
Return: object -> web server starting
"""


from app.server import create_app as server
from app.server.data import db, ma, create_db

app = server()

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        create_db()
        db.create_all()
    app.run('0.0.0.0')