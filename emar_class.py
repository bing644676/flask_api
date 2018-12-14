#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime


# 广告主
class Client(object):
    def __init__(self, params):
        if 'client_id' in params and params['client_id'] != '':
            self.client_id = params['client_id']
        if 'client_name' in params and params['client_name'] != '':
            self.client_name = params['client_name']
        if 'homepage' in params and params['homepage'] != '':
            self.homepage = params['homepage']
        if 'category' in params and params['category'] != '':
            self.category = params['category']
        if 'address' in params and params['address'] != '':
            self.address = params['address']
        if 'qualifications' in params and params['qualifications'] != '':
            self.qualifications = eval(params['qualifications'])
        if 'domains' in params and params['domains'] != '':
            self.domains = eval(params('domains'))
        if 'qq' in params and params['qq'] != '':
            self.qq = params['qq']
        if 'province' in params and params['province'] != '':
            self.province = params['province']
        if 'city' in params and params['city'] != '':
            self.city = params['city']
        if 'phone' in params and params['phone'] != '':
            self.phone = params['phone']


# 广告
class Creative(object):
    def __init__(self, params):
        if 'creative_id' in params and params['creative_id'] != '':
            self.creative_id = str(params['creative_id'])
        if 'creative_name' in params and params['creative_name'] != '':
            self.creative_name = params['creative_name']
        if 'client_id' in params and params['client_id'] != '':
            self.client_id = params['client_id']
        now = datetime.datetime.now()
        if 'start_date' in params and params['start_date'] != '':
            self.start_date = params['start_date']
        # else:
        #     self.start_date = now.strftime('%Y%m%d')
        if 'end_date' in params and params['end_date'] != '':
            self.end_date = params['end_date']
        # else:
        #     self.end_date = (now + datetime.timedelta(days=30)).strftime('%Y%m%d')
        if 'category' in params and params['category'] != '':
            self.category = str(params['category'])
        if 'banner_info' in params and params['banner_info'] != '':
            self.banner = params['banner_info']

        if 'native_info' in params and params['native_info'] != '':
            self.native = params['native_info']

        if 'landing_page' in params and params['landing_page'] != '':
            self.landing_page = params['landing_page']
        if 'impr_monitor_url' in params and params['impr_monitor_url'] != '':
            self.impr_monitor_url = params['impr_monitor_url']
        if 'click_monitor_url' in params and params['click_monitor_url'] != '':
            self.click_monitor_url = params['click_monitor_url']
        if 'deeplink' in params and params['deeplink'] != '':
            self.deeplink = params['deeplink']
