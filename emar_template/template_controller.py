#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import logging
import logging.handlers
from flask_restful import Resource
from emar_config import *
from emar_template.template_model import EmarTemplate, session, Advertiser, Creative, Campaign, Channel, Crowd
from emar_template.template_parser import *
from emar_template.template_response import get_json, advertiser_json, creative_json, campaign_json, channel_json, crowd_json
from emar_mysql import DbMysql, Rds
from emar_pubilc import create_id, get_creative_id, get_campaign_id, channel_crowd

mdb = DbMysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
mdb.connect()

rds = Rds(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD)
rds.connect_rds()


# 创建channel（post/get）资源列表
class CrowdList(Resource):
    # 添加认证
    # decorators = [auth.login_required]

    @staticmethod
    def get(action):
        result = {'code': 200, 'message': "ok", 'data': {}}
        if action == 'all':
            args = crowd_get.parse_args()
            task_list = session.query(Crowd)
            if task_list:
                res_list = [crowd_json(task) for task in task_list]
                result['data']['totalCount'] = len(res_list)
                result['data']['list'] = res_list
            else:
                result['data']['totalCount'] = 0
            return result, 200
        else:
            result['code'] = 404
            result['message'] = '你访问的网页不存在'
        return result, 404

    @staticmethod
    def post(action):
        if action == 'add':
            args = crowd_post.parse_args()
            # 构建新数据
            args['crowd_id'] = channel_crowd(rds, 'crowd')
            tasks = Crowd(crowd_id=args['crowd_id'], crowd_name=args['crowd_name'], status=args['status'])
            try:
                session.add(tasks)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'add crowd ok', 'data': crowd_json(tasks)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'add channel failed'}, 500
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404


# 创建channel（post/get）资源列表
class ChannelList(Resource):
    # 添加认证
    # decorators = [auth.login_required]

    @staticmethod
    def get(action):
        result = {'code': 200, 'message': "ok", 'data': {}}
        if action == 'all':
            args = channel_get.parse_args()
            task_list = session.query(Channel)
            if task_list:
                res_list = [channel_json(task) for task in task_list]
                result['data']['totalCount'] = len(res_list)
                result['data']['list'] = res_list
            else:
                result['data']['totalCount'] = 0
            return result, 200
        else:
            result['code'] = 404
            result['message'] = '你访问的网页不存在'
        return result, 404

    @staticmethod
    def post(action):
        if action == 'add':
            args = channel_post.parse_args()
            # 构建新数据
            args['channel_id'] = channel_crowd(rds, 'channel')
            tasks = Channel(channel_id=args['channel_id'], channel_name=args['channel_name'], status=args['status'])
            try:
                session.add(tasks)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'add channel ok', 'data': channel_json(tasks)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'add channel failed'}, 500
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404


# 创建campaign（post/get）资源列表
class CampaignList(Resource):
    # 添加认证
    # decorators = [auth.login_required]

    @staticmethod
    def get(action):
        """
        :param action: 
        :return: 
        query查询 curl http://127.0.0.1:5000/campaign/query -X GET -d "advertiser_id=1000020000000700000" 
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        list查询 curl http://127.0.0.1:5000/campaign/list -X GET -d "page=1&size=1" 
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        args = campaign_get.parse_args()
        tasks = session.query(Campaign)
        task_list = None
        result = {'code': 200, 'message': "ok"}
        if action == 'query':
            if args['advertiser_id'] is not None:
                task_list = tasks.filter(Campaign.advertiser_id == args['advertiser_id'])
                if task_list:
                    logging.info('creative task_list: {0}'.format(task_list))
                    result['data'] = campaign_json(task_list[0])
                else:
                    result['data'] = ''
                return result, 200
            else:
                result['code'] = 400
                result['message'] = 'need advertiser_id data'
                return result, 400
        elif action == 'list':
            if args['page'] is None or args['size'] is None:
                result = {'code': 400, 'message': "need page and size data"}
                return result, 400

            page = args['page']
            size = args['size']
            result['data'] = {'totalPage': 0, 'totalCount': 0}
            if args['name'] is None:
                task_list = tasks.filter(Campaign.creative_name != '')
                # 返回结果
                if task_list:
                    res_list = [campaign_json(task) for task in task_list]
                    length = len(res_list)
                    if size >= length:
                        result['data']['totalPage'] = 1
                        result['data']['totalCount'] = length
                        if page > 1:
                            result['data']['list'] = []
                        else:
                            result['data']['list'] = res_list
                    else:
                        total_page = int(length / size) + 1
                        result['data']['totalPage'] = total_page
                        if page > total_page:
                            res = []
                        elif page == total_page:
                            res = res_list[(page - 1) * size:]
                        else:
                            res = res_list[((page - 1) * size): (page * size)]
                        result['data']['totalCount'] = len(res)
                        result['data']['list'] = res
                return result, 200
            else:
                task_list = tasks.filter(Campaign.creative_name.like('%{0}%'.format(args['name'])))
                result['data'] = {'totalPage': 0, 'totalCount': 0, 'list': []}
                # 返回结果
                if task_list:
                    res_list = [campaign_json(task) for task in task_list]
                    length = len(res_list)
                    if size >= length:
                        result['data']['totalPage'] = 1
                        result['data']['totalCount'] = length
                        result['data']['list'] = res_list
                    else:
                        total_page = int(length / size) + 1
                        result['data']['totalPage'] = total_page
                        if page == total_page:
                            res = res_list[(page - 1) * size:]
                        else:
                            res = res_list[((page - 1) * size): (page * size)]
                        result['data']['totalCount'] = len(res)
                        result['data']['list'] = res
                return result, 200
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404

    @staticmethod
    def post(action):
        """
        :param action: 
        :return: dict
        添加活动 curl http://127.0.0.1:5000/campaign/add -X POST -d "advertiser_id=1000020000000000000&
        creative_name=jikestar_model&category=87&platform=2&budget=1200&price=0.4&status=0&adx_ids=[1,2]&
        speed=0&creatives=[123,231]" -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        
        更新活动 curl http://127.0.0.1:5000/campaign/update -X POST -d "advertiser_id=1000020000000700000&
        creative_name=jikestar_model_131w&category=87&platform=2&budget=1200&price=0.4&status=0&
        adx_ids=[1,2]&speed=0&creatives=[123,231]"
         -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        """

        if action == 'add':
            args = campaign_post.parse_args()
            # 构建新数据
            advertiser_id = get_campaign_id(mdb, rds, args['advertiser_id'])
            args['advertiser_id'] = advertiser_id
            tasks = Campaign(advertiser_id=args['advertiser_id'],
                             creative_name=args['creative_name'],
                             category=args['category'],
                             platform=args['platform'],
                             budget=args['budget'],
                             price=args['price'],
                             status=args['status'],
                             adx_ids=args['adx_ids'],
                             speed=args['speed'],
                             start_date=args['start_date'],
                             end_date=args['end_date'],
                             week_hours=args['week_hours'],
                             areas=args['areas'],
                             ip_list=args['ip_list'],
                             device_brand=args['device_brand'],
                             device_price=args['device_price'],
                             connection=args['connection'],
                             os=args['os'],
                             lbs=args['lbs'],
                             crowds=args['crowds'],
                             creatives=args['creatives'],
                             )
            try:
                session.add(tasks)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'add campaign ok', 'data': campaign_json(tasks)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'add campaign failed'}, 500
        elif action == 'update':
            args = campaign_post.parse_args()
            advertiser_id_set = set([campaign.advertiser_id for campaign in session.query(Campaign.advertiser_id)])
            print(advertiser_id_set, args['advertiser_id'])
            if args['advertiser_id'] not in advertiser_id_set:
                return {'code': 400, 'message': '输入的广告活动id不存在'}, 400
            campaign = session.query(Campaign).filter(Campaign.advertiser_id == args['advertiser_id'])[0]
            campaign.advertiser_id = args['advertiser_id']
            campaign.creative_name = args['creative_name']
            campaign.category = args['category']
            campaign.platform = args['platform']
            campaign.budget = args['budget']
            campaign.price = args['price']
            campaign.status = args['status']
            campaign.adx_ids = args['adx_ids']
            campaign.speed = args['speed']
            campaign.start_date = args['start_date']
            campaign.end_date = args['end_date']
            campaign.week_hours = args['week_hours']
            campaign.areas = args['areas']
            campaign.ip_list = args['ip_list']
            campaign.device_brand = args['device_brand']
            campaign.device_price = args['device_price']
            campaign.connection = args['connection']
            campaign.os = args['os']
            campaign.lbs = args['lbs']
            campaign.crowds = args['crowds']
            campaign.creatives = args['creatives']
            try:
                session.merge(campaign)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'update campaign ok', 'data': campaign_json(campaign)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'update campaign failed'}, 500
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404


# 创建creative（post/get/put)资源列表
class CreativeList(Resource):
    # 添加认证
    # decorators = [auth.login_required]

    @staticmethod
    def get(action):
        """
        :param action: 
        :return: dict
        query curl http://127.0.0.1:5000/creative/query -X GET -d "creative_id=1000020000000000002" 
        -H "Authorization:  token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        args = creative_get.parse_args()
        tasks = session.query(Creative)
        task_list = None
        result = {'code': 200, 'message': "ok"}
        if action == 'query':
            if args['creative_id'] is not None:
                task_list = tasks.filter(Creative.creative_id == args['creative_id'])
                if task_list:
                    logging.info('creative task_list: {0}'.format(task_list))
                    result['data'] = creative_json(task_list[0])
                else:
                    result['data'] = ''
                return result, 200
            else:
                result['code'] = 400
                result['message'] = 'need creative_id data'
                return result, 400
        elif action == 'list':
            if args['page'] is None or args['size'] is None:
                result = {'code': 400, 'message': "need page and size data"}
                return result, 400

            page = args['page']
            size = args['size']
            result['data'] = {'totalPage': 0, 'totalCount': 0}
            if args['name'] is None:
                task_list = tasks.filter(Creative.creative_name != '')
                # 返回结果
                if task_list:
                    res_list = [creative_json(task) for task in task_list]
                    length = len(res_list)
                    if size >= length:
                        result['data']['totalPage'] = 1
                        result['data']['totalCount'] = length
                        if page > 1:
                            result['data']['list'] = []
                        else:
                            result['data']['list'] = res_list
                    else:
                        total_page = int(length / size) + 1
                        result['data']['totalPage'] = total_page
                        if page > total_page:
                            res = []
                        elif page == total_page:
                            res = res_list[(page - 1) * size:]
                        else:
                            res = res_list[((page - 1) * size): (page * size)]
                        result['data']['totalCount'] = len(res)
                        result['data']['list'] = res
                return result, 200
            else:
                task_list = tasks.filter(Creative.creative_name.like('%{0}%'.format(args['name'])))
                result['data'] = {'totalPage': 0, 'totalCount': 0, 'list': []}
                # 返回结果
                if task_list:
                    res_list = [creative_json(task) for task in task_list]
                    length = len(res_list)
                    if size >= length:
                        result['data']['totalPage'] = 1
                        result['data']['totalCount'] = length
                        result['data']['list'] = res_list
                    else:
                        total_page = int(length / size) + 1
                        result['data']['totalPage'] = total_page
                        if page == total_page:
                            res = res_list[(page - 1) * size:]
                        else:
                            res = res_list[((page - 1) * size): (page * size)]
                        result['data']['totalCount'] = len(res)
                        result['data']['list'] = res
                return result, 200
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404

    @staticmethod
    def post(action):
        """
        添加创意 curl http://127.0.0.1:5000/creative/add -X POST -d "advertiser_id=1000020000000000000&
        creative_name=rise&creative_type=2&creative_url=http://material-mm.oss-cn-beijing.aliyuncs.com/rise
        /kxj_1200x627.jpg&width=1200&height=627&url=http://material-mm.oss-cn-bei&landing_page=http://material-
        mm.oss-cn-beijing.aliyuncs.com/rise/kxj_1200x627.jpg&status=0" 
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"

        更新创意 curl http://127.0.0.1:5000/creative/update -X POST -d "creative_id=1000020000000000002&
        advertiser_id=1000020000000000000&creative_name=jikestar&creative_type=2&creative_url=http://material-mm.
        oss-cn-beijing.aliyuncs.com/rise/kxj_1200x627.jpg&width=1200&height=627&url=http://material-mm.oss-cn-bei
        &landing_page=http://material-mm.oss-cn-beijing.aliyuncs.com/rise/kxj_1200x627.jpg&status=0" 
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        if action == 'add':
            args = creative_post.parse_args()
            # 构建新数据
            advertising_id = get_creative_id(mdb, rds, args['advertiser_id'])
            args['creative_id'] = advertising_id
            tasks = Creative(advertiser_id=args['advertiser_id'],
                             creative_id=args['creative_id'],
                             creative_name=args['creative_name'],
                             creative_type=args['creative_type'],
                             creative_url=args['creative_url'],
                             width=args['width'],
                             height=args['height'],
                             url=args['url'],
                             size=args['size'],
                             landing_page=args['landing_page'],
                             title=args['title'],
                             image_type=args['image_type'],
                             video_duration=args['video_duration'],
                             extra=args['extra'],
                             impr_monitor_url=args['impr_monitor_url'],
                             click_monitor_url=args['click_monitor_url'],
                             deeplink=args['deeplink'],
                             desc=args['desc'],
                             status=args['status']
                             )
            try:
                session.add(tasks)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'add creative ok', 'data': creative_json(tasks)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'add creative failed'}, 500
        elif action == 'update':
            args = creative_post.parse_args()
            creative_id_set = set([creative.creative_id for creative in session.query(Creative.creative_id)])
            if args['creative_id'] not in creative_id_set:
                return {'code': 400, 'message': '输入的广告创意id不存在'}, 400
            creative = session.query(Creative).filter(Creative.creative_id == args['creative_id'])[0]
            creative.advertiser_id = args['advertiser_id']
            creative.creative_id = args['creative_id']
            creative.creative_name = args['creative_name']
            creative.creative_type = args['creative_type']
            creative.creative_url = args['creative_url']
            creative.width = args['width']
            creative.height = args['height']
            creative.url = args['url']
            creative.size = args['size']
            creative.landing_page = args['landing_page']
            creative.title = args['title']
            creative.image_type = args['image_type']
            creative.video_duration = args['video_duration']
            creative.extra = args['extra']
            creative.impr_monitor_url = args['impr_monitor_url']
            creative.click_monitor_url = args['click_monitor_url']
            creative.deeplink = args['deeplink']
            creative.desc = args['desc']
            creative.status = args['status']
            try:
                session.merge(creative)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'update creative ok', 'data': creative_json(creative)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'update creative failed'}, 500
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404


# 操作advertiser(post/get)资源列表
class AdvertiserList(Resource):
    # 添加认证
    # decorators = [auth.login_required]

    @staticmethod
    def get(action):
        """
        获取一个数据: curl http://127.0.0.1:5000/advertiser/query -X GET -d "advertiser_id=1000010000000000000"
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        获取多条数据: curl http://127.0.0.1:5000/advertiser/list -X GET -d "page=2&size=2" 
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        根据name获取多条数据: curl http://127.0.0.1:5000/advertiser/list -X GET -d "page=2&size=2&ri" 
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        args = advertiser_get.parse_args()
        tasks = session.query(Advertiser)
        task_list = None
        if action == 'query':
            if 'advertiser_id' in args and args['advertiser_id']:
                task_list = tasks.filter(Advertiser.advertiser_id == args['advertiser_id'])
                logging.info('task_list:{0}'.format(task_list))
                if task_list:
                    result = {'code': 200,
                              'message': "ok",
                              'data': advertiser_json(task_list[0])}
                    return result, 200
            else:
                result = {'code': 400, 'message': "need advertiser_id data"}
                return result, 400
        elif action == 'all':
            result = {'code': 200,
                      'message': "ok",
                      'data': {'totalCount': 0}}
            res_list = [advertiser_json(task) for task in tasks]
            if res_list:
                result['data']['totalCount'] = len(res_list)
                result['data']['list'] = res_list
            return result
        elif action == 'list':
            if args['page'] is None or args['size'] is None:
                result = {'code': 400, 'message': "need page and size data"}
                return result, 400

            page = args['page']
            size = args['size']
            if args['name'] is None:
                task_list = tasks.filter(Advertiser.advertiser_name != '')
                # 返回结果
                if task_list:
                    result = {'code': 200,
                              'message': "ok",
                              'data': {'totalPage': 0, 'totalCount': 0}}
                    res_list = [advertiser_json(task) for task in task_list]
                    length = len(res_list)
                    if size >= length:
                        result['data']['totalPage'] = 1
                        result['data']['totalCount'] = length
                        if page > 1:
                            result['data']['list'] = []
                        else:
                            result['data']['list'] = res_list
                    else:
                        total_page = int(length / size) + 1
                        result['data']['totalPage'] = total_page
                        if page > total_page:
                            res = []
                        elif page == total_page:
                            res = res_list[(page - 1) * size:]
                        else:
                            res = res_list[((page - 1) * size): (page * size)]
                        result['data']['totalCount'] = len(res)
                        result['data']['list'] = res
                    return result, 200
                return {'code': 400, 'message': "访问结果不存在"}, 400
            else:
                task_list = tasks.filter(Advertiser.advertiser_name.like('%{0}%'.format(args['name'])))
                # 返回结果
                if task_list:
                    result = {'code': 200,
                              'message': "ok",
                              'data': {'totalPage': 1, 'totalCount': 0, 'list': []}}
                    res_list = [advertiser_json(task) for task in task_list]
                    length = len(res_list)
                    if size >= length:
                        result['data']['totalCount'] = length
                        result['data']['list'] = res_list
                    else:
                        total_page = int(length / size) + 1
                        result['data']['totalPage'] = total_page
                        if page == total_page:
                            res = res_list[(page - 1) * size:]
                        else:
                            res = res_list[((page - 1) * size): (page * size)]
                        result['data']['totalCount'] = len(res)
                        result['data']['list'] = res
                    return result, 200
                return {'code': 400, 'message': "访问结果不存在"}, 400

        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404

    @staticmethod
    def post(action):
        """
        添加广告主:curl http://127.0.0.1:5000/advertiser/add -X POST -d "advertiser_name=rise&site_name=瑞思学科英语
        &url=http://www.risecenter.com&connector=孙一丁&phone=13011110000&category=87&qualifications=
        {'5001001': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/bp.jpeg',
        '5001002': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/icp.jpg',
        '5001021': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/brand.jpeg',
        '5001091': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/eq.jpeg'}"
        -H "Authorization:  token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        if action == 'add':
            args = advertiser_post.parse_args()
            # 构建新数据
            advertiser_id, advertising_id = create_id("emar", args['advertiser_name'], mdb, rds, method='hget')

            args['advertiser_id'] = advertiser_id

            tasks = Advertiser(advertiser_name=args['advertiser_name'], site_name=args['site_name'], url=args['url'],
                               connector=args['connector'], phone=args['phone'], email=args['email'],
                               address=args['address'], brand=args['brand'], category=args['category'],
                               qualifications=args['qualifications'], qq=args['qq'], province=args['province'],
                               city=args['city'], advertiser_id=args['advertiser_id'])
            try:
                session.add(tasks)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'add advertiser ok', 'data': advertiser_json(tasks)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'add task failed'}, 500
        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404

    @staticmethod
    def put(action):
        """
        更新广告主:curl http://127.0.0.1:5000/advertiser/update -X PUT -d "advertiser_name=rise&site_name=瑞思学科英语
        &url=http://www.risecenter.com&connector=孙一丁&phone=13011110000&category=87&qualifications=
        {'5001001': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/bp.jpeg',
        '5001002': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/icp.jpg',
        '5001021': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/brand.jpeg',
        '5001091': 'https://qualifications.oss-cn-beijing.aliyuncs.com/rise/eq.jpeg'}"
        -H "Authorization:  token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        if action == 'update':
            args = advertiser_put.parse_args()
            advertiser_id_set = set(
                [advertiser.advertiser_id for advertiser in session.query(Advertiser.advertiser_id)])
            if args['advertiser_id'] not in advertiser_id_set:
                return {'code': 400, 'message': '输入的广告主id不存在'}, 400
            advertiser = session.query(Advertiser).filter(Advertiser.advertiser_id == args['advertiser_id'])[0]
            advertiser.advertiser_name = args['advertiser_name']
            advertiser.site_name = args['site_name']
            advertiser.url = args['url']
            advertiser.connector = args['connector']
            advertiser.phone = args['phone']
            advertiser.email = args['email']
            advertiser.address = args['address']
            advertiser.brand = args['brand']
            advertiser.category = args['category']
            advertiser.qualifications = args['qualifications']
            advertiser.qq = args['qq']
            advertiser.province = args['province']
            advertiser.city = args['city']
            advertiser.advertiser_id = args['advertiser_id']

            try:
                session.merge(advertiser)
                session.commit()
                # 资源添加成功，返回200
                result = {'code': 200, 'message': 'update advertiser ok', 'data': advertiser_json(advertiser)}
                return result, 200
            except Exception as err:
                session.rollback()
                logging.error(traceback.format_exc())
                logging.error(err)
                return {'code': 500, 'message': 'update advertiser failed'}, 500

        else:
            return {'code': 404, 'message': '你访问的网页找不到'}, 404


# 操作emar_template(post/get)资源列表
class EmarTemplateList(Resource):
    # 添加认证
    # decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        获取一个数据: curl http://127.0.0.1:5000/task/ -X GET -d "template_id=512010&width_height=640x960"
        -H "Authorization: token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        args = parser_get.parse_args()
        tasks = session.query(EmarTemplate)
        task_list = None
        if args['template_id'] and args['width_height']:
            task_list = tasks.filter(EmarTemplate.template_id == args['template_id'],
                                     EmarTemplate.width_height == args['width_height'])
        elif args['width_height']:
            task_list = tasks.filter(EmarTemplate.width_height == args['width_height'])
        elif args['template_id']:
            task_list = tasks.filter(EmarTemplate.template_id == args['template_id'])
        else:
            task_list = tasks.filter(EmarTemplate.template_id != '')
        logging.info('task_list:{0}'.format(task_list))
        if task_list.count() == 0:
            return 'there is no task', 404
        # 返回结果
        return [get_json(task) for task in task_list], 200

    @staticmethod
    def post():
        """
        添加一个数据:curl http://127.0.0.1:5000/task/ -X POST -d "template_id=512010&width_height=640x960
        &picture_width=640&picture_height=960&picture_size=30"
        -H "Authorization:  token 2343fe43jias34df5hue34fs53afsa734ref"
        """
        args = parser_post.parse_args()

        # 构建新数据
        tasks = EmarTemplate(template_id=args['template_id'], width_height=args['width_height'],
                             picture_width=args['picture_width'], picture_height=args['picture_height'],
                             picture_size=args['picture_size'])
        try:
            session.add(tasks)
            session.commit()
            # 资源添加成功，返回200
            return get_json(tasks), 200
        except Exception as err:
            session.rollback()
            logging.error(traceback.format_exc())
            logging.error(err)
            return {'code': 500, 'message': 'update advertiser failed'}, 500
