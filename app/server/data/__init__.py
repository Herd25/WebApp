#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Database init

Keyword arguments: none
argument -- description
Return: object -> database finally created
"""

# Global Imports
from app.server.data.static import db, ma
from app.server.data.models import Table, Schema
from flask import current_app as app

def create_db():
    engine = db.create_engine(app.config['ENGINE_URI'], {})
    engine.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['DB_NAME']}")

class TableExample(Table):
    '''Create Table Example 
    Keyword arguments: Table
    argument -- description 
    Return: object -> Return Table object '''
    
    def __init__(self,):
        super(Table,self).__init__()