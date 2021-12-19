#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports
from app.server.helpers.web.api import Api

def url_routes(**kwargs):
    """sumary_line
    
    Keyword arguments: (blueprint, noun, table, schema, login, custom_login, endpoints)
    argument -- blueprint or object flask app
    Return: Objects -> Return url Endpoints
    """
    
    login = kwargs.get('login', {})

    view = Api.as_view(
        f"{kwargs.get('noun')}_api",
        kwargs.get('table'),
        kwargs.get('schema')
    )

    endpoints = kwargs.get(
        'endpoints',
        get_endpoint(
            kwargs.get('noun'),
            kwargs.get('login', False)
        )
    )

    for i in endpoints:
        kwargs.get('blueprint').add_url_rule(
            i[0],
            methods=i[1],
            view_func=view
        )

def get_endpoint(noun: str, loggin: bool) -> list:
    list = [
        [f'/api/{noun}/', ['POST', 'GET']],
        [f'/api/{noun}/<int:id>', ['GET', 'PUT', 'DELETE']]
    ]
    if loggin:
        list.insert(0, [f'/api/{noun}/login', ['POST']])

    return list
