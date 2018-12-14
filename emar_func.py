#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import requests
from emar_config import ID, TOKEN
from emar_class import Client, Creative


# emar_template服务接口
def get_template(template_id=None, width_height=''):
    result = []
    headers = {'Authorization': 'token 2343fe43jias34df5hue34fs53afsa734ref'}
    url = 'http://127.0.0.1:5000/task/'
    if template_id and width_height:
        params = {'template_id': template_id, 'width_height': width_height}
    elif template_id:
        params = {'template_id': template_id}
    elif width_height:
        params = {'width_height': width_height}
    else:
        params = {}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
    return result


def send_request(url, params):
    response = None
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    data = {'id': ID, 'token': TOKEN}
    data.update(params)
    print(data)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


# 广告主上传与修改接口
def upload_client(items):
    url = 'http://api.emarbox.com/client/upload'
    params = {'client': Client(items).__dict__}
    return url, params


# 广告主查询接口
def query_client(client_id):
    url = 'http://api.emarbox.com/client/query'
    params = {'client_id': client_id}
    return url, params


# 广告上传与修改接口
def upload_creative(items):
    url = 'http://api.emarbox.com/creative/upload'
    params = {'creative': Creative(items).__dict__}
    return url, params


# 广告查询接口
def query_creative(client_id, creative_id):
    url = 'http://api.emarbox.com/creative/query'
    params = {'client_id': client_id, 'creative_id': creative_id}
    return url, params


# 广告审核状态查询接口
def creative_status(client_id, creative_id):
    url = 'http://api.emarbox.com/creative/status'
    params = {'client_id': client_id, 'creative_id': creative_id}
    return url, params


# 投放数据查询接口, date的时间格式YYYY-MM-DD
# level 查询的数据级别(1 - 广告主级别，3 - 广告级别)
def query_report(date, level, client_id='', creative_id=''):
    url = 'http://api.emarbox.com/report/query'
    params = {'date': date, 'level': level}
    if client_id != '':
        params['client_id'] = client_id
    if creative_id != '':
        params['creative_id'] = creative_id
    return url, params
