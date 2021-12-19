#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global Imports
from flask import Flask
from app.config.constant.httpd import *

def server(config : object, *args):
    """ Create Server Application
    
    Keyword arguments:
    argument -- (config, blueprints) * Objects configuration from master aplication
    Return: app -> is object 
    """
    
    app = Flask(__name__)
    app.config.from_object(config)
    error_handlers(app)
    blueprints(app)
    extensions(app)
    
    return app

def error_handlers(app : Flask):
    """ Register Error Handlers from app
    
    Keyword arguments: app -> Flask Object
    argument -- keyword from perosnalize flask error Handlers
    Return: object -> Boolean
    """
    from flask import jsonify

    # * Methods from error page

    # * Error 404
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({'Message' : 'this page could not be found!'}), HTTP_404_NOT_FOUND

    # * Error 405
    @app.errorhandler(405)
    def not_allowed(err):
        return jsonify({'Message' : 'this method is not allowed for the request url!'}), HTTP_405_METHOD_NOT_ALLOWED
    
    # * Error 401
    @app.errorhandler(401)
    def not_unauthorized(err):
        return jsonify({'Authenticated' : 'Could not Verify!'}), HTTP_401_UNAUTHORIZED

def blueprints(app : Flask, *bluep):
    """ Register application Blueprint
    
    Keyword arguments: (app, blueprints)
    argument -- Register flask master application and blueprints form app
    Return: object -> Url create from api server
    """
    for blueprint in bluep:
        app.register_blueprint(blueprint)

def extensions(app : Flask):
    """ Register Api Extensions
    
    Keyword arguments: app -> Flask instance
    argument -- require app from init extension from SQLAlchemy and Marshmallow
    Return: object -> Boolean
    """
    from .data import create_db
    from .data.static import db, ma

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        #create_db()
        db.create_all()