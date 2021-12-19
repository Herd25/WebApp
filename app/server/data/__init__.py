#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports
from flask import current_app as app
from app.server.data.static import db, ma
from app.server.data.models import Table, Notes
class Users(Table):
    ''' Create Table Example 
    Keyword arguments: Table
    argument -- create user table and instance 
    Return: object -> Return Table object '''
    
    def __init__(self,):
        super(Table,self).__init__()

class Note(Notes):
    ''' Create table Notes 
    Keyword arguments: none
    argument -- create note table and instance 
    Return: object -> Return Note object''' 

    def __init__(self,):
        super(Notes,self).__init__()

def create_db():
    engine = db.create_engine(app.config['EGINE_URI'], {})
    engine.execute('CREATE DATABASE IF NOT EXISTS {}'.format(app.config["DB_NAME"]))

def create_user():
    default = Table.query.filter_by(id=1).first()
        
    if not default:
        neew = Table({
                "name" : "alex",
                "email" : "alex@mail.com",
                "password" : "alex12",
                "all_perm" : True
            })
        neew.save()
    print('Default user in db!')