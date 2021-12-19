#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Exmaples Routes

Keyword arguments: (blueprint_name)
argument -- creation blueprint for web server
Return: boolean -> views for app
"""

# Global Imports
from flask import Blueprint

users = Blueprint('users', __name__)
notes = Blueprint('notes', __name__)

