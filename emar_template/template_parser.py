#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import reqparse

# template RESTfulAPI的参数解析 -- post参数解析
parser_post = reqparse.RequestParser()
parser_post.add_argument("template_id", type=int, required=True, help="need template_id data")
parser_post.add_argument("width_height", type=str, required=True, help="need width_height data")
parser_post.add_argument("picture_width", type=int, required=True, help="need picture_width data")
parser_post.add_argument("picture_height", type=int, required=True, help="need picture_height data")
parser_post.add_argument("picture_size", type=int, required=True, help="need picture_size data")

# template RESTfulAPI的参数解析 -- get参数解析
parser_get = reqparse.RequestParser()
parser_get.add_argument("template_id", type=int, required=False)
parser_get.add_argument("width_height", type=str, required=False)

# Advertiser RESTfulAPI的参数解析 -- post参数解析
advertiser_post = reqparse.RequestParser()
advertiser_post.add_argument('advertiser_name', type=str, required=True, help="need advertiser_name data")
advertiser_post.add_argument('site_name', type=str, required=True, help="need site_name data")
advertiser_post.add_argument('url', type=str, required=True, help="need url data")
advertiser_post.add_argument('connector', type=str, required=True, help="need connector data")
advertiser_post.add_argument('phone', type=str, required=True, help="need phone data")
advertiser_post.add_argument('email', type=str, required=False)
advertiser_post.add_argument('address', type=str, required=False)
advertiser_post.add_argument('brand', type=str, required=False)
advertiser_post.add_argument('category', type=int, required=True, help="need category data")
advertiser_post.add_argument('qualifications', type=str, required=True, help="need qualifications data")
advertiser_post.add_argument('qq', type=str, required=False)
advertiser_post.add_argument('province', type=str, required=False)
advertiser_post.add_argument('city', type=str, required=False)
advertiser_post.add_argument('advertiser_id', type=str, required=False)

# Advertiser RESTfulAPI的参数解析 -- get参数解析
advertiser_get = reqparse.RequestParser()
advertiser_get.add_argument("advertiser_id", type=str, required=False)
advertiser_get.add_argument("page", type=int, required=False)
advertiser_get.add_argument("size", type=int, required=False)
advertiser_get.add_argument("name", type=str, required=False)

# Advertiser RESTfulAPI的参数解析 -- put参数解析
advertiser_put = reqparse.RequestParser()
advertiser_put.add_argument("advertiser_id", type=str, required=True, help="need advertiser_id data")
advertiser_put.add_argument('advertiser_name', type=str, required=True, help="need advertiser_name data")
advertiser_put.add_argument('site_name', type=str, required=True, help="need site_name data")
advertiser_put.add_argument('url', type=str, required=True, help="need url data")
advertiser_put.add_argument('connector', type=str, required=True, help="need connector data")
advertiser_put.add_argument('phone', type=str, required=True, help="need phone data")
advertiser_put.add_argument('email', type=str, required=False)
advertiser_put.add_argument('address', type=str, required=False)
advertiser_put.add_argument('brand', type=str, required=False)
advertiser_put.add_argument('category', type=int, required=True, help="need category data")
advertiser_put.add_argument('qualifications', type=str, required=True, help="need qualifications data")
advertiser_put.add_argument('qq', type=str, required=False)
advertiser_put.add_argument('province', type=str, required=False)
advertiser_put.add_argument('city', type=str, required=False)

# Creative RESTfulAPI的参数解析 -- post参数解析
creative_post = reqparse.RequestParser()
creative_post.add_argument("advertiser_id", type=str, required=True, help="need advertiser_id data")
creative_post.add_argument("creative_id", type=str, required=False)
creative_post.add_argument("creative_name", type=str, required=True, help="need creative_name data")
creative_post.add_argument("creative_type", type=int, required=True, help="need creative_type data")
creative_post.add_argument("creative_url", type=str, required=False)
creative_post.add_argument("width", type=int, required=True, help="need width data")
creative_post.add_argument("height", type=int, required=True, help="need height data")
creative_post.add_argument("url", type=str, required=True, help="need url data")
creative_post.add_argument("size", type=int, required=False, help="need size data")
creative_post.add_argument("landing_page", type=str, required=True, help="need landing_page data")
creative_post.add_argument("title", type=str, required=False)
creative_post.add_argument("image_type", type=int, required=False)
creative_post.add_argument("video_duration", type=int, required=False)
creative_post.add_argument("extra", type=str, required=False)
creative_post.add_argument("impr_monitor_url", type=str, required=False)
creative_post.add_argument("click_monitor_url", type=str, required=False)
creative_post.add_argument("deeplink", type=str, required=False)
creative_post.add_argument("desc", type=str, required=False)
creative_post.add_argument("status", type=str, required=True, help="need status data")

# Creative RESTfulAPI的参数解析 -- get参数解析
creative_get = reqparse.RequestParser()
creative_get.add_argument("creative_id", type=str, required=False)
creative_get.add_argument("page", type=int, required=False)
creative_get.add_argument("size", type=int, required=False)
creative_get.add_argument("name", type=str, required=False)

# Campaign RESTfulAPI的post参数解析
campaign_post = reqparse.RequestParser()
campaign_post.add_argument("advertiser_id", type=int, required=True,
                           help="need advertiser_id data")
campaign_post.add_argument("creative_name", type=str, required=True,
                           help="need creative_name data")
campaign_post.add_argument("category", type=int, required=True, help="need category data")
campaign_post.add_argument("platform", type=int, required=True, help="need platform data")
campaign_post.add_argument("budget", type=int, required=True, help="need budget data")
campaign_post.add_argument("price", type=float, required=True, help="need price data")
campaign_post.add_argument("status", type=int, required=True, help="need status data")
campaign_post.add_argument("adx_ids", type=str, required=True, help="need adx_ids data")
campaign_post.add_argument("speed", type=int, required=True, help="need speed data")
campaign_post.add_argument("start_date", type=str, required=False)
campaign_post.add_argument("end_date", type=str, required=False)
campaign_post.add_argument("week_hours", type=str, required=False)
campaign_post.add_argument("areas", type=str, required=False)
campaign_post.add_argument("ip_list", type=str, required=False)
campaign_post.add_argument("device_brand", type=str, required=False)
campaign_post.add_argument("device_price", type=str, required=False)
campaign_post.add_argument("connection", type=str, required=False)
campaign_post.add_argument("os", type=str, required=False)
campaign_post.add_argument("lbs", type=str, required=False)
campaign_post.add_argument("crowds", type=str, required=False)
campaign_post.add_argument("creatives", type=str, required=True, help="need creatives data")

# Campaign RESTfulAPI的get参数解析
campaign_get = reqparse.RequestParser()
campaign_get.add_argument("advertiser_id", type=int, required=False)
campaign_get.add_argument("page", type=int, required=False)
campaign_get.add_argument("size", type=int, required=False)
campaign_get.add_argument("name", type=str, required=False)

# Channel RESTfulAPI的get参数解析
channel_get = reqparse.RequestParser()

# Channel RESTfulAPI的post参数解析
channel_post = reqparse.RequestParser()
channel_post.add_argument("channel_id", type=int, required=False)
channel_post.add_argument("channel_name", type=str, required=True, help="need channel_name data")
channel_post.add_argument("status", type=int, required=False, default=1)

# Crowd RESTfulAPI的get参数解析
crowd_get = reqparse.RequestParser()

# Channel RESTfulAPI的post参数解析
crowd_post = reqparse.RequestParser()
crowd_post.add_argument("crowd_id", type=int, required=False)
crowd_post.add_argument("crowd_name", type=str, required=True, help="need crowd_name data")
crowd_post.add_argument("status", type=int, required=False, default=1)
