#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports

from flask import current_app as app
from flask import jsonify, request
from jwt import jwt
from functools import wraps
from app.server.data import TableExample
from marshmallow import ValidationError

"""Decorator from auth

Keyword arguments: schema, current_user, token
argument -- token validation form api server
Return: objetc -> return token from api
"""

def token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'Message' : 'Token is Missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Table.query.filter_by(id=data['id']).first()
        except jwt.ExpiredSignature:
            return jsonify({'Message' : 'Token is invalid!'}), 401

        return fn(*args, current_user, **kwargs)

    return wrapper

def validate(schema: object):
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

