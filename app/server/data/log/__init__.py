#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# * Global Imports
from app.server.data import ma
from marshmallow import validate

class Login(ma.Schema):
    ''' Login Schema 
    Keyword arguments: ma.Schema
    argument -- Object ma Marshmallow Schema 
    Return: object ->  email and password ''' 
    def __init__(self):
        self.email = ma.Email(required = True)
        self.password = ma.Str(validate = validate.Length(min=8), required = True)