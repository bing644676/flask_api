#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import logging
import logging.handlers
from emar_config import *
from emar_mysql import DbMysql


def get_code(mdb, adx, advertiser):
    adx_code = ''
    advertiser_code = ''
    adx_sql = "select adx_code from adx_info where `adx`= '{0}'".format(adx)
    advertiser_sql = """select advertiser_code from advertiser_info where `advertiser` = '{0}'""".format(advertiser)
    adx_codes = mdb.query(adx_sql)
    advertiser_codes = mdb.query(advertiser_sql)
    if len(adx_codes) != 0:
        adx_code = adx_codes[0][0]
    if len(advertiser_codes) != 0:
        advertiser_code = str(advertiser_codes[0][0]).zfill(6)
    return adx_code, advertiser_code


def get_middle():
    middle_num = '000000'
    return middle_num


# adx占2位,广告主占6位，中间值占6位，自增量5位
def create_id(adx, advertiser, mdb, rds, method='hincrby'):
    advertiser_id = 0

    adx_code, advertiser_code = get_code(mdb, adx, advertiser)
    middle_num = get_middle()

    advertiser_end_num = str(advertiser_id).zfill(5)
    if method == 'hget':
        advertising_end_num = str(rds.rds_hget(adx, advertiser)).zfill(5)
    else:
        advertising_end_num = str(rds.rds_hincr(adx, advertiser, 1)).zfill(5)
    advertiser_id = '{0}{1}{2}{3}'.format(adx_code, advertiser_code, middle_num, advertiser_end_num)
    advertising_id = '{0}{1}{2}{3}'.format(adx_code, advertiser_code, middle_num, advertising_end_num)
    return advertiser_id, advertising_id


def get_name(mdb, advertiser_id):
    adx_name = ''
    advertiser_name = ''
    adx_code = str(advertiser_id)[:2]
    advertiser_code = int(str(advertiser_id)[2:8])
    adx_sql = "select adx from adx_info where adx_code={0}".format(adx_code)
    advertiser_sql = "select advertiser from advertiser_info where advertiser_code={0}".format(advertiser_code)
    adx_names = mdb.query(adx_sql)
    advertiser_names = mdb.query(advertiser_sql)
    if adx_names:
        adx_name = adx_names[0][0]
    if advertiser_names:
        advertiser_name = advertiser_names[0][0]
    return adx_name, advertiser_name


def get_creative_id(mdb, rds, advertiser_id):
    adx, advertiser = get_name(mdb, advertiser_id)
    advertising_end_num = str(rds.rds_hincr(adx, advertiser, 1)).zfill(5)
    advertising_index = advertiser_id[:14]
    creative_id = '{0}{1}'.format(advertising_index, advertising_end_num)
    return creative_id


def get_campaign_id(mdb, rds, advertiser_id):
    adx, advertiser = get_name(mdb, advertiser_id)
    end_num = '00000'
    middle_id = str(rds.rds_hincr(adx, 'campaign', 1)).zfill(6)
    advertising_index = str(advertiser_id)[:8]
    campaign_id = '{0}{1}{2}'.format(advertising_index, middle_id, end_num)
    return campaign_id


def channel_crowd(rds, name):
    c_id = 100000
    if name == 'channel':
        end_num = rds.rds_hincr('channel', 'channel_id', 1)
        c_id += int(end_num)
    elif name == 'crowd':
        end_num = rds.rds_hincr('crowd', 'crowd_id', 1)
        c_id += int(end_num)
    return c_id


def initlog(log_file):
    loginstance = logging.getLogger()
    hdlr = logging.handlers.TimedRotatingFileHandler(log_file, when='H', interval=1, backupCount=40)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    loginstance.addHandler(hdlr)
    loginstance.setLevel(logging.NOTSET)
    return loginstance
