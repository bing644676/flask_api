#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
# from flask import g
# from flask_httpauth import HTTPTokenAuth


MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 13306
MYSQL_USER = 'md'
MYSQL_PASSWORD = 'maida6868'
MYSQL_DB = 'dsp_advertising'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 21601
REDIS_DB = 2
REDIS_PASSWORD = 'Mindata123'

ID = '102616'
TOKEN = '935C25792A58C382291114951572897A'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_USER = "maimeng"
MONGO_PASSWORD = "maimeng"
MONGO_DB = "maimeng"
MONGO_TABLE = "test_table"

'''
auth = HTTPTokenAuth(scheme="token")
TOKENS = {"2343fe43jias34df5hue34fs53afsa734ref"}


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        g.current_user = token
        return True
    return False
'''