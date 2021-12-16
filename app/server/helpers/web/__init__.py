#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Create Routes Standar

Keyword arguments:
argument -- description
Return: return_description
"""

# Global Imports
from app.server.helpers.web.api import Api

def url_routes(table: object, schema: object, blueprints: object, noun: str, loggin: bool = False):
    view = Api.as_view(
        f"{noun}_api",
        table,
        schema
    )
    endpoints = get_endpoint(noun, loggin)
    for i in endpoints:
        blueprints.add_url_rule(
            i[0],
            methods=i[1],
            view_func=view
        )

def get_endpoint(noun: str, loggin: bool):
    list = [
        [f'/api/{noun}/', ['POST', 'GET']],
        [f'/api/{noun}/<int:_id>', ['GET', 'PUT', 'DELETE']]
    ]
    if loggin:
        list.insert(0, [f'/api/{noun}/login', ['POST']])

    return list
