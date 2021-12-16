#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

""" - Server Create app Context

Keyword arguments: none
argument -- create webapp
Return: app -> server create isntance
"""

# Global Imports
from flask import Flask, jsonify
from app.config.constant.httpd import *
from app.config import Dev
from app.server.helpers.web.routes import example

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    
    # * Methods from error page
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({'Message' : 'this page could not be found!'}), HTTP_404_NOT_FOUND

    @app.errorhandler(405)
    def not_allowed(err):
        return jsonify({'Message' : 'this method is not allowed for the request url!'}), HTTP_405_METHOD_NOT_ALLOWED


    if test_config is None:
        app.config.from_object(Dev)

    app.register_blueprint(example)

    return app

