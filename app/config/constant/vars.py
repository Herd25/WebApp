#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""GLOBAL SYSTEM VARS

Keyword arguments: none
argument -- flask vars
Return: none
"""
import os

# Flask vars default
DEB = False
TEST= False
PATH = os.path.dirname(os.path.abspath(__file__))
KEY = os.urandom(16)
DB = "database.db"
ENGINE = "sqlite:///" + os.path.join(PATH,f'{DB}')
ROUTE = ENGINE
MODIFICATONS = False