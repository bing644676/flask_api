#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import g
from flask_httpauth import HTTPTokenAuth


MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 13306
MYSQL_USER = 'md'
MYSQL_PASSWORD = 'maida6868'
MYSQL_DB = 'dsp_advertising'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 21601
REDIS_DB = 2
REDIS_PASSWORD = 'Mindata123'

auth = HTTPTokenAuth(scheme="token")
TOKENS = {"2343fe43jias34df5hue34fs53afsa734ref"}


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        g.current_user = token
        return True
    return False
