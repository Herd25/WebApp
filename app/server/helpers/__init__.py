#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Blueprints and helpers start

Keyword arguments: none
argument -- start web server routing
Return: objects -> objects and Methods views
"""

# Global Imports
from app.server.helpers.web.routes import example
from app.server.helpers.web import url_routes
from app.server.data import TableExample, Schema

url_routes(TableExample, Schema, example, "example", True)



