#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""
 # Global Imports

from app.config.constant.vars import *
import os

class Init(object):
  DEBUG = DEB
  TESTING = TEST


class Dev(Init):
  APP_ROOT = os.path.dirname(os.path.abspath(__file__))
  DEGUB = True
  SECRET_KEY = os.urandom(16)
  DB_NAME = "database"
  TESTING = True
  EGINE_URI = 'sqlite:///' + os.path.join(APP_ROOT, DB_NAME + '.db')
  SQLALCHEMY_DATABASE_URI = f'{EGINE_URI}'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

