#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc

db = SQLAlchemy()
ma = Marshmallow()

class Base(object):
    ''' Data standard Models
    Keyword arguments: db
    argument -- normal functions in database 
    Return: object -> return status from database ''' 

    @classmethod
    def save(self) -> bool:
        db.session.add(self)

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def get_by_id(table, id, *args):
        return db.session.query(table).get_or_404(id)

    @staticmethod
    def all(table, *args):
        return db.session.query(table).all()

    @classmethod
    def delete(self, *args) -> bool:
        db.session.delete(self)

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True