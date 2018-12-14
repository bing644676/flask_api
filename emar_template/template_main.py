#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import argparse
import logging.config
from flask import Flask
from flask_restful import Api
from emar_template.template_controller import EmarTemplateList, AdvertiserList, CreativeList,\
    CampaignList, ChannelList, CrowdList

# Flask相关变量声明
app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=True))
api = Api(app)


api.add_resource(EmarTemplateList, '/task/')
api.add_resource(AdvertiserList, '/advertiser/<string:action>')
api.add_resource(CreativeList, '/creative/<string:action>')
api.add_resource(CampaignList, '/campaign/<string:action>')
api.add_resource(ChannelList, '/channels/<string:action>')
api.add_resource(CrowdList, '/crowds/<string:action>')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', help='日志配置', default='config/logging.conf')
    args = parser.parse_args()

    if args.logging:
        os.makedirs('log', exist_ok=True)
        logging.config.fileConfig(args.logging)
    app.run(port=5000)
