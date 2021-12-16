#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""
 # Global Imports

from app.config.constant.vars import *

class Init(object):
  DEBUG = DEB
  TESTING = TEST
  APP_ROOT = PATH
  SECRET_KEY = KEY
  DB_NAME = DB
  SQLALCHEMY_TRACK_MODIFICATIONS = MODIFICATONS


class Dev(Init):
  DEGUB = True
  TESTING = True
  SQLALCHEMY_DATABASE_URI = ROUTE

