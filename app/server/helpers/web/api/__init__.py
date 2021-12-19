#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

# Global imports
from flask import jsonify, request, abort
from flask.views import MethodView
import jwt
import datetime
from flask import current_app as app
from app.config.constant.httpd import *
from app.server.helpers.auth import auth, token
from app.server.data import ma, db
from app.server.data.log import Login

class Api(MethodView):
    ''' Global Control Endpoints and Methods 
    Keyword arguments: MethodView
    argument -- MethodViews class from rules endpoints 
    Return: object -> rules from endpoints ''' 

    def __init__(self, table: db.Model, table_schema: ma.Schema, **kwargs):
        self.custom_login = kwargs
        self.Table = table
        self.result = table_schema()
        self.Results = table_schema(many=True)
        self.login = auth(kwargs.get("schema", Login) ())(self.login)
        self.put = auth(self.result)(self.put)
        self.add = auth(self.result)(self.add)

    @classmethod
    @token()
    def get(self, current_user : object, id : int = None):
        """ Method HTTP GET
        
        Keyword arguments: (current_user, id), 
        argument -- current_user and id Params from get Method Api
        Return: JSON, httpd_status_code -> Return objects from http Response
        """
        
        if id:
            return self.get_id(current_user, id)

        elif 'page' in request.args.keys():
            page = int(request.args.get(
                'page',
                type=int,
                default=1
            ))
            per_page = int(request.args.get(
                'size',
                type=int,
                default=10
            ))
            return self.pagination(page, per_page, current_user)
        return self.get_all(current_user)

    @classmethod
    def get_id(self, current_user : object, id : int ):
        registry = self.Table.get_by_id(self.Table, id, current_user)
        return self.result.jsonify(registry)

    @classmethod
    def get_all(self, current_user : object):
        list = self.Table.all(self.Table, current_user)
        return jsonify({'Results' : self.Results.dump(list)}), HTTP_200_OK

    @classmethod
    def pagination(self, page : int, per_page : int, current_user : object):
        paginate = self.Table.paginate(self.Table, page, per_page, current_user)
        return jsonify({'Results' : self.Results.dump(paginate.items),
        'Total-Pages' : paginate.pages}), HTTP_200_OK

    @classmethod
    def post(self):
        """ Method HTTP POST
        
        Keyword arguments: Null
        argument -- Return Login User And POST HTTP Request
        Return: Boolean -> Return True of False for LoginUser and Authorized API
        """

        rute = str(request.url_rule)
        if rute.find('login') != -1:
            return self.login()
        return self.add()

    @classmethod
    def login(self):
        """ Created and New Session and execute POST Request
        
        Keyword arguments: null
        argument -- Return AUTH JSON
        Return: token(jwt) : Object -> JSON Object
        """
        auth = request.json()
        field_name = self.custom_login.get(
            'field_search',
            "email"
        )
        field_value = auth[field_name]
        search_dict = {field_name : field_value}

        user = self.Table.query.filter_by(**search_dict).first()

        if not user:
            abort(401)

        password_field = self.custom_login.get(
            'password_field',
            "password"
        )

        password = auth[password_field]

        if user.compare_password(password):
            token = jwt.encode({
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, self.custom_login.get('key_encript', app.config['SECRET_KEY']))
            action = self.custom_login.get('post_action', False)

            if action:
                exec(f'action[0]({action[1]})')
            return jsonify({'Token' : token.decode('UTF-8')}), HTTP_201_CREATED
        abort(401)
        

    @classmethod
    @token()
    def add(self, current_user : object):
        """ Add New Record!
        
        Keyword arguments: current_user
        argument -- Add New Record in database
        Return: Boolean
        """

        new = self.Table(request.json, current_user)
        insert = new.save()
        if not insert:
            return self.database_err()
        return self.result.jsonify(new), HTTP_201_CREATED

    @classmethod
    @token()
    def put(self, current_user : object, id : int):
        """ Edit Record in Database
        
        Keyword arguments: (current_user, id)
        argument -- current users object and id fro update database Records
        Return: Boolean
        """
        
        update = self.Table.get_by_id(self.Table, id, current_user)
        update.changes(request.json, current_user)
        insert = update.save()
        if not insert:
            return self.database_err("update")
        return self.result.jsonify(update), HTTP_202_ACCEPTED

    @classmethod
    @token()
    def delete(self, current_user: object, id : int):
        """ Delete Records 
        
        Keyword arguments: (current_user, id)
        argument -- current_user object and id from delete Records in database
        Return: Boolean
        """
        
        delt = self.Table.get_by_id(self.Table, id, current_user)
        data = delt.delete(current_user)
        if not data:
            return self.database_err('delete')
        return self.result.jsonify(delt)

    @staticmethod
    def database_err(action: str = 'insert') -> jsonify:
        return jsonify({'Err' : f'Error trying is{action} data!'}), HTTP_409_CONFLICT