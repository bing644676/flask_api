#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import logging
import traceback
from emar_pubilc import initlog
from emar_func import *
from api_deal_xlsx import *
from emar_mysql import DbMysql, Rds
from emar_config import *
from emar_pubilc import create_id

log_file = './log/emar_api.log'
logger = initlog(log_file)


# 创建banner广告
def create_banner(material_info, adx_name, advertiser, mdb, rds, items, operation, task):
    flag = True
    for material in material_info:
        if material['type'] == 'logo':
            continue
        width = material['width']
        height = material['height']
        banner_url = material['url']
        banner_info = {'width': width, 'height': height, 'url': banner_url}
        advertiser_id, advertising_id = create_id(adx_name, advertiser, mdb, rds)
        items['client_id'] = advertiser_id
        items['creative_id'] = advertising_id
        items['banner_info'] = banner_info
        url, params = upload_creative(items)
        response = send_request(url, params)
        if response.status_code == 200:
            result = response.json()
            if 'ret_code' in result and result['ret_code'] == 0:
                res = rds.rds_hset(adx_name, advertising_id, advertiser_id)
                flag &= res
                logger.info("save the {0} to redis's result is {1}".format(advertising_id, res))
            logger.info("{0} {1}'s result is {2}".format(operation, task, result))
        else:
            logger.error("{0} {1} failed".format(operation, task))
            logger.error(traceback.format_exc())
            flag &= False
    return flag


# 创建native广告
def create_native(material_info, adx_name, advertiser, mdb, rds, items, operation, task):
    flag = True
    for material in material_info:
        if material['type'] == 'logo':
            continue
        width = material['width']
        height = material['height']
        width_height = '{0}x{1}'.format(width, height)
        template_list = get_template(width_height=width_height)
        if len(template_list) == 0:
            continue

        for template in template_list:
            advertiser_id, advertising_id = create_id(adx_name, advertiser, mdb, rds)
            items['client_id'] = advertiser_id
            items['creative_id'] = advertising_id
            native_info = {'template_id': template['template_id']}
            native_info.setdefault('images', {})
            native_info['images'] = {template['picture_code']: material['url']}
            if 'logo_code' in template and template['logo_flag'] != '':
                for info in material_info:
                    if info['type'] == 'logo' and info['width'] == int(template['logo_width']) and \
                                    info['height'] == int(template['logo_height']):

                        native_info['images'].update({template['logo_code']: info['url']})
            texts = {}
            # 标题最短4个字符，最长12个字符
            if 'title_flag' in template and template['title_flag'] != '':
                texts['title'] = items['title']
            # 长描述最长30个字符， 短描述最长13个字符
            if 'description_flag' in template and template['description_flag'] == "是":
                desc_len = int(template['description_size'].split('-')[1])
                if desc_len < 17:
                    texts['description'] = items['short_desc']
                else:
                    texts['description'] = items['long_desc']

            if texts:
                native_info['texts'] = texts

            # 按钮名称，字符范围2-4
            if 'button_flag' in template and template['button_flag'] == '是':
                native_info['button_name'] = items['button_name']

            items['native_info'] = native_info

            url, params = upload_creative(items)

            response = send_request(url, params)

            if response.status_code == 200:
                result = response.json()
                print(result)
                if 'ret_code' in result and result['ret_code'] == 0:
                    res = rds.rds_hset(adx_name, advertising_id, advertiser_id)
                    flag &= res
                    logger.info("save the {0} to redis's result is {1}".format(advertising_id, res))
                logger.error("{0} {1}'s result is {2}".format(operation, task, result))
            else:
                logger.error("{0} {1} failed".format(operation, task))
                logger.error(traceback.format_exc())
                flag &= False
    return flag


def main():
    opts, args = getopt.getopt(sys.argv, "h", ["help"])
    if len(args) < 4:
        print("Usage: python3 {0} create|update client|creative client_file|creative_file "
              "[opt:material_file]".format(args[0]))
        sys.exit(-1)

    operation = args[1]
    task = args[2]
    task_file = args[3]
    rows = read_excel_file(task_file)
    items = deal_row(rows)


    mdb = DbMysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    mdb.connect()

    rds = Rds(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD)
    rds.connect_rds()
    if operation == 'create':
        adx_name = items['adx_name']
        advertiser = items['advertiser']

        if task == 'client':
            advertiser_id, advertising_id = create_id(adx_name, advertiser, mdb, rds, "hget")
            items['client_id'] = advertiser_id
            # 由于接口类型为id不存在创建，存在就更新，故先判断广告主id是否存在，若存在且审核通过，提醒谨慎更新。
            client_id = items['client_id']
            query_url, query_params = query_client(client_id)

            response = send_request(query_url, query_params)
            print(response.status_code)
            if response.status_code == 200:
                result = response.json()

                if 'audit' in result and result['audit'] == 1:
                    flag = input('the client_id {0} Existing and approved, '
                                 'Are you sure you want to update it? yes or no:'.format(client_id))
                    if flag != "yes":
                        sys.exit(-1)
                    operation = 'update'
                else:
                    print('result:', result)

            url, params = upload_client(items)
            response = send_request(url, params)
            print(response.json())
            if response.status_code == 200:
                result = response.json()
                # 将广告主id记录到hash，待检测审核通过存入mongodb
                if 'ret_code' in result and result['ret_code'] == 0:
                    res = rds.rds_hset(adx_name, advertiser_id, advertiser_id)
                    logger.info("save the {0} to redis's result is {1}".format(advertiser_id, res))
                logger.info("{0} {1}'s result is {2}".format(operation, task, result))
        elif task == 'creative':
            if len(args) < 4:
                logger.info("Usage: python3 {0} creative creative_file material_file".format(args[0]))
                sys.exit(-1)

            material_file = args[4]

            material_data = read_excel_file(material_file)
            material_info = deal_line(material_data)

            # 判断广告类型banner or native 默认全部创建
            creative_type = items['creative_type']
            res_flag = True
            if creative_type == 1:
                banner_flag = create_banner(material_info, adx_name, advertiser, mdb, rds, items, operation, task)
                res_flag &= banner_flag
            elif creative_type == 2:

                native_flag = create_native(material_info, adx_name, advertiser, mdb, rds, items, operation, task)
                res_flag &= native_flag
            else:
                banner_flag = create_banner(material_info, adx_name, advertiser, mdb, rds, items, operation, task)
                native_flag = create_banner(material_info, adx_name, advertiser, mdb, rds, items, operation, task)
                res_flag &= (banner_flag & native_flag)
            logger.info("create the creative's result is {0}".format(res_flag))
        else:
            logger.info("The task only supports client and creative. Please make sure the spelling is correct")
            sys.exit(-1)

    elif operation == 'update':
        if task == 'client':
            url, params = upload_client(items)
            response = send_request(url, params)
            if response.status_code == 200:
                result = response.json()
                if 'ret_code' in result and result['ret_code'] == 100:
                    res = rds.rds_hset(items['adx_name'], items['client_id'], items['client_id'])
                    logger.info("save the {0} to redis's result is {1}".format(items['client_id'], res))
                logger.info("{0} {1}'s result is {2}".format(operation, task, result))
            else:
                logger.info("{0} {1} failed".format(operation, task))
                logger.info(traceback.format_exc())
        elif task == 'creative':
            if len(args) < 4:
                logger.info("Usage: python3 {0} creative creative_file material_file".format(args[0]))
                sys.exit(-1)
            material_file = args[3]

            material_data = read_excel_file(material_file)
            material_info = deal_line(material_data)

            creative_id = items['creative_id']
            client_id = items['client_id']
            url, params = query_creative(client_id, creative_id)
            response = send_request(url, params)
            if response.status_code == 200:
                result = response.json()
                if 'creative' in result and result['creative'] != '':
                    items = result['creative']
                    if 'native' in items:
                        template_id = items['native']['template_id']
                        templates = get_template(template_id=template_id)
                        for template in templates:
                            for material in material_info:
                                if material['picture_width'] == template['picture_width'] and \
                                                material['picture_height'] == template['picture_height']:
                                    native_info = {'template_id': template['template_id']}
                                    native_info.setdefault('images', {})
                                    native_info['images'] = {template['picture_code']: material['url']}
                                    if 'logo_code' in template and template['logo_code'] != '':
                                        for info in material_info:
                                            if info['type'] == 'logo' and info['width'] == template['logo_width'] and \
                                                            info['height'] == template['logo_height']:
                                                native_info['images'].update({template['logo_code']: info['url']})
                                                break
                                    texts = {}
                                    # 标题最短4个字符，最长12个字符
                                    if 'title_flag' in template and template['title_flag'] != '':
                                        texts['title'] = items['title']
                                    # 长描述最长30个字符， 短描述最长13个字符
                                    if 'description_flag' in template and template['description_flag'] == "是":
                                        desc_len = int(template['description_size'].split('-')[1])
                                        if desc_len < 17:
                                            texts['description'] = items['short_desc']
                                        else:
                                            texts['description'] = items['long_desc']
                                    # 着落页
                                    if 'landing_page_flag' in template and template['landing_page_flag'] != '':
                                        texts['landing_page'] = items['landing_page']
                                    if texts:
                                        native_info['texts'] = texts
                                    items['native_info'] = native_info
                                    url, params = upload_creative(items)
                                    response = send_request(url, params)
                                    if response.status_code == 200:
                                        result = response.json()
                                        if 'ret_code' in result and result['ret_code'] == 0:
                                            res = rds.rds_hset(items['adx_name'], creative_id, client_id)
                                            logger.info(
                                                "save the {0} to redis's result is {1}".format(client_id, res))
                                        logger.info("{0} {1}'s result is {2}".format(operation, task, result))
                                    else:
                                        logger.error("{0} {1} failed".format(operation, task))
                                        logger.error(traceback.format_exc())
        else:
            logger.error("The task only supports client and creative. Please make sure the spelling is correct")
    else:
        logger.error("The task only supports create and update. Please make sure the spelling is correct")


if __name__ == '__main__':
    main()
