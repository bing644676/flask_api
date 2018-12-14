#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
from emar_func import *
from emar_mysql import *
from emar_config import *
from emar_pubilc import *
from api_deal_xlsx import *

log_file = './log/emar_to_mongo.log'
logger = initlog(log_file)


def extra_info():
    info = {}
    return info


def get_name(mdb, advertiser_code, adx_name):
    my_dic = {}
    advertiser_sql = "select advertiser from advertiser_info where advertiser_code = {0}".format(advertiser_code)
    adx_sql = "select adx from adx_code where adx_name = '{0}'".format(adx_name)
    advertisers = mdb.query(advertiser_sql)
    adxs = mdb.query(adx_sql)
    if len(advertisers) != 0:
        my_dic['advertiser_name'] = advertisers[0]
    if len(adxs) != 0:
        my_dic['adx_code'] = adxs[0]
    return my_dic


def main():
    opts, args = getopt.getopt(sys.argv, "h", ["help"])
    if len(args) < 3:
        logger.error("Usage: python3 {0} adx_name".format(args[0]))
        sys.exit(-1)
    adx_name = args[1]

    rds = Rds(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD)
    rds.connect_rds()

    mongodb = MongoDB(MYSQL_HOST, MONGO_PORT, MYSQL_USER, MONGO_PASSWORD, MONGO_DB, MONGO_TABLE, 'creative_id')
    mongodb.connect()

    mdb = DbMysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    mdb.connect()

    # hash的field为adx_name，key为广告， value为广告主
    advertings = rds.rds_hkey(adx_name)
    for adverting in advertings:
        # 广告主
        if adverting[-5:] == '00000':
            continue
        else:
            advertiser = rds.rds_hget(adx_name, adverting)
            url, params = query_creative(advertiser, adverting)
            response = send_request(url, params)
            if response.status_code == 200:
                result = response.json()
                if 'audit' in result and result['audit'] == 0:
                    infos = result['creative']
                    infos['adx_name'] = adx_name
                    infos['advertiser_id'] = int(adverting[2:8])
                    my_dic = get_name(mdb, adx_name, infos['advertiser_id'])
                    if my_dic:
                        infos.update(my_dic)
                    infos['advertiser_name'] = "rise"
                    extra_infos = extra_info()
                    if extra_infos:
                        infos.update(extra_infos)
                    key = {'creative_id': infos['creative_id']}
                    if 'native' in infos:
                        infos['advertising_type'] = 'native'
                    elif 'banner' in infos:
                        infos['advertising_type'] = 'banner'
                    # update or insert
                    res = mongodb.update(key, infos)
                    if res:
                        logging.info("save {0} to mongodb's result is {1}".format(infos, res))
                        rds.rds_hdel(adverting, advertiser)
                    else:
                        logging.error(traceback.extract_stack())
                else:
                    logging.info("the {0} {1} failed to pass the audit".format(advertiser, adverting))
            else:
                logging.error(traceback.extract_stack())
                break


if __name__ == '__main__':
    main()
