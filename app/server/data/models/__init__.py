#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports
from app.server.data.static import db, ma, Base
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate

# * Class User Model
class Table(db.Model, Base):
    '''sumary_line 
    Keyword arguments: users
    argument -- user models and schema 
    Return: table for user data ''' 
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    all_perm = db.Column(db.Boolean, nullable=False, default=False)
    
    def __init__(self, fields: dict, current_user: object = None):
        self.changes(fields, current_user)

    @classmethod
    def changes(self, fields: dict, current_user: object):
        self.name = fields.get('name')
        self.password = self.__generate_password(fields.get('password'))
        self.email = fields.get('email')
        self.all_perm = fields.get('all_perm')
        print(current_user)

    @classmethod
    def delete(self, current_user):
        if current_user.all_perm:
            return super().delete()
        return False

    @staticmethod
    def __generate_password(passwd: str) -> str:
        return generate_password_hash(passwd)

    @classmethod
    def compare_password(self, passwd: str) -> bool:
        return check_password_hash(self.password, passwd)

class Schema(ma.Schema):
    '''sumary_line 
    Keyword arguments: ma
    argument -- User Schema 
    Return: objects -> json data result '''
    
    name = ma.Str(validate = validate.Length(min=1), required = True)
    email = ma.Email(required = True)
    password = ma.Str(validate = validate.Length(min=4), load_only = True, required = True)
    all_perm = ma.Bool(load_only = True, required = False)
    
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'all_perm')

# * Class notes Model
class Notes(db.Model, Base):
    '''sumary_line 
    Keyword arguments: notes
    argument -- Notes Model Schema 
    Return: notes database ''' 
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    content = db.Column(db.String(240), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, fields: dict, current_user: object):
        self.changes(fields, current_user)

    @classmethod
    def changes(self, fields: dict, current_user: object):
        self.name = fields.get('name')
        self.content = fields.get('content')
        self.id_user = current_user.id

    @classmethod
    def delete(self, current_user):
        if current_user.id == self.id_user:
            return super().delete()
        return False

class NoteSchema(ma.Schema):
    name = ma.Str(validate = validate.Length(min=1), required = True)
    content = ma.Str(validate = validate.Length(min=1), required = True)
    class Meta:
        fields = ('id', 'name', 'content')