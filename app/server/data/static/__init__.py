#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Data standard Models

Keyword arguments: sdb
argument -- class Standard from models in Database
Return: object -> return sqlalchemy query
"""

# Global Imports
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc

db = SQLAlchemy()
ma = Marshmallow()

class Base(object):
    '''sumary_line 
    Keyword arguments: db
    argument -- normal functions in database 
    Return: object -> return status from database ''' 
    def __init__(self,):
        pass

    @classmethod
    def save(self,):
        db.session.add(self)

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    @classmethod
    def delete(self,):
        db.session.delete(self)

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            return False
        return True