#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports

from flask import current_app as app
from flask import jsonify, request
import jwt
from functools import wraps
from marshmallow import ValidationError
from app.server.data import ma
from app.config.constant.httpd import HTTP_401_UNAUTHORIZED

"""Decorator from auth

Keyword arguments: schema, current_user, token
argument -- token validation form api server
Return: object -> return token from api
"""

def token(**params):
    """ Validate jwt Token
    
    Keyword arguments: Arbitrary keywords arguments
    argument -- Register user Lookup Table Default to app config
    Return: key -> key jwt token generate from app.config['SECRET_KEY']
    """
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            token : str = request.headers.get('x-access-token', None)

            if not token:
                return jsonify({'Message' : '?.. Token is Missign!!'}), HTTP_401_UNAUTHORIZED

            table = params.get('table', app.config['TABLE_VALIDATE_TOKEN'])
            key = params.get('key', app.config['SECRET_KEY'])

            try:
                data = jwt.decode(token, key)
                current_user = table.query.filter_by(id=data['id']).first()
            except (jwt.ExpiredSignature, jwt.InvalidSignatureError, jwt.DecodeError):
                return jsonify({'Message' : 'Token is invalid!'}), HTTP_401_UNAUTHORIZED

            return fn(*args, current_user, **kwargs)

        return wrapper
    return inner

def auth(schema: ma.Schema):
    """ Validate JSON send
    
    Keyword arguments: ma.Schema : Marshmallow schema from validate JSON
    argument -- Marshmallow schema from validate JSON
    Return: object -> return JSON for auth Users
    """
    
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.json)
            except ValidationError as err:
                return err.messages

            return f(*args, **kwargs)

        return wrapper
    return inner

