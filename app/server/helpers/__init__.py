#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Blueprints and helpers start

Keyword arguments: (table, schema, blueprint, noun, login)
argument -- start web server routing
Return: objects -> objects and Methods views
"""

# Global Imports
from app.server.helpers.web.routes import users, notes
from app.server.helpers.web import url_routes
from app.server.data import Users, Note
from app.server.data.models import Schema, NoteSchema

url_routes(table=Users, schema=Schema, blueprint=users, noun="users", custom_login=True)
url_routes(table=Note, schema=NoteSchema, blueprint=notes, noun="notes")



