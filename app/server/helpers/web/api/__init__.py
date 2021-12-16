#!/usr/bin/env pyhton3
#-*- coding: utf-8 -*-

"""Invoke Pyhton Flask server

Keyword arguments:
argument -- description
Return: return_description
"""
# Global imports
from flask import jsonify, request
from flask.views import MethodView
import jwt
import datetime
from flask import current_app as app
from app.server.helpers.auth import validate, token
from app.config.constant.httpd import *

class Api(MethodView):
    '''sumary_line 
    Keyword arguments: 
    argument -- description 
    Return: return_description ''' 

    def __init__(self, table, table_schema):
        self.Table = table
        self.result = table_schema()
        self.Results = table_schema(many=True)
        self.put = validate(self.result)(self.put)
        self.add = validate(self.result)(self.add)
        self.not_found = jsonify({'Message' : 'Record Not Found!'}), HTTP_404_NOT_FOUND

    @classmethod
    @token
    def get(self, current_user, id = None):
        self.not_exists = jsonify({'Message' : 'Not are items from search!'}), HTTP_404_NOT_FOUND

        if id:
            registry = self.Table.query.filter_by(id=id).first()
            if registry:
                return self.result.jsonify(registry)
            return self.not_exists
        else:
            search = request.args.to_dict()
            if 'page' in search.keys():
                page = int(search['page'])
                per_page = int(search['size']) if 'size' in search.keys() else 10
                paginate = self.Table.query.paginate(page, per_page, False)
                if not paginate.items:
                    return self.not_exists
                return jsonify(
                    {'Result' : self.Results.dump(paginate.items),
                    'Pages' : paginate.items
                    }), HTTP_200_OK
            else:
                all = self.Table.query.all()
                if not all:
                    return self.not_exists
                return self.Results.jsonify(all)

    @classmethod
    def post(self,):
        rute = str(request.url_rule)
        if rute.find('login') != -1:
            auth = request.json
            err = jsonify({'Message' : 'Error not auth Token Verify'}), HTTP_401_UNAUTHORIZED
            if not auth or not auth['name'] or not auth['password']:
                return err

            table = self.Table.query.filter_by(name=auth['name']).first()

            if not table:
                return err

            if table.compare_password(auth['password']):
                token = jwt.encode({
                    'id' : table.id,
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
                }, app.config['SECRET_KEY'])
                return jsonify({'Token' : token.decode('UTF-8')}), HTTP_201_CREATED
            return err
        else:
            return self.add()

    @classmethod
    @token
    def add(self, current_user, id):
        new = self.Table(request.json)
        insert = new.save()
        if not insert:
            return self.database_err()
        return self.result.jsonify(insert), HTTP_201_CREATED

    @classmethod
    @token
    def put(self, current_user, id):
        update = self.Table.query.get(id)
        if not update:
            return self.not_exists
        update.changes(request.json)
        data = update.save()
        if not data:
            return self.database_err('update')
        return self.result.jsonify(update), HTTP_202_ACCEPTED

    @classmethod
    @token
    def delete(self, current_user, id):
        delt = self.Table.query.get(id)
        if not delt:
            return self.not_exists
        data = delt.delete()
        if not data:
            return self.database_err('delete')
        return self.result.jsonify(delt)

    @staticmethod
    def database_err(action: str = 'insert') -> jsonify:
        return jsonify({
            'Err' : f'Error trying is{action} data!',
            'Posibilities' : {
                '1' : 'Data integrity error.',
                '2' : 'Could not connect to DB.',
                '3' : 'The action could not be performed due to an error in request.',
                '4' : 'Some other Error.',
            }
            }), HTTP_400_BAD_REQUEST