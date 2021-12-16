#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Model Example

Keyword arguments:
argument -- Global Model Database
Return: object -> query database
"""

# Global Imports
from app.server.data.static import db, ma, Base
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate

class Table(object):
    '''sumary_line 
    Keyword arguments: 
    argument -- description 
    Return: return_description ''' 
    __tablename__ = 'TableExample'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def __init__(self, fields: dict):
        self.changes(fields)

    @classmethod
    def changes(self, fields: dict):
        self.name = fields['name']
        self.password = self.__generate_password(fields['password'])
        self.email = fields['email']

    @staticmethod
    def __generate_password(passwd: str) -> str:
        return generate_password_hash(passwd)

    @classmethod
    def compare_password(self, passwd: str) -> bool:
        return check_password_hash(self.password, passwd)

class Schema(ma.Schema):
    '''sumary_line 
    Keyword arguments: 
    argument -- description 
    Return: return_description '''
    
    name = ma.Str(validate = validate.Length(min=1), required = True)
    email = ma.Email(required = True)
    password = ma.Str(validate = validate.Length(min=4), load_only = True, required = True)
    
    class Meta:
        fields = ('id', 'name', 'email', 'password')