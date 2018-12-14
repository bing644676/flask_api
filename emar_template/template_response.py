#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def channel_json(channel):
    channel_info = dict(channel_id=channel.channel_id, channel_name=channel.channel_name, status=channel.status)
    return channel_info


def crowd_json(crowd):
    crowd_info = dict(crowd_id=crowd.crowd_id, crowd_name=crowd.crowd_name, status=crowd.status)
    return crowd_info


def campaign_json(campaign):
    """
    构建campaign数据模型的json格式
    :param campaign: 
    :return: dict
    """
    campaign_info = dict(advertiser_id=campaign.advertiser_id, creative_name=campaign.creative_name,
                         category=campaign.category, platform=campaign.platform, budget=campaign.budget,
                         price=campaign.price, status=campaign.status, adx_ids=campaign.adx_ids, speed=campaign.speed,
                         start_date=campaign.start_date, end_date=campaign.end_date, week_hours=campaign.week_hours,
                         areas=campaign.areas, ip_list=campaign.ip_list, device_brand=campaign.device_brand,
                         device_price=campaign.device_price, connection=campaign.connection, os=campaign.os,
                         lbs=campaign.lbs, crowds=campaign.crowds, creatives=campaign.creatives)
    return campaign_info


def creative_json(creative):
    """
    构建advertiser数据模型的json格式
    :param creative
    :return: dict
    """
    creative_info = dict(advertiser_id=creative.advertiser_id, creative_id=creative.creative_id,
                         creative_name=creative.creative_name, creative_type=creative.creative_type,
                         creative_url=creative.creative_url, width=creative.width, height=creative.height,
                         url=creative.url, size=creative.size, landing_page=creative.landing_page, title=creative.title,
                         image_type=creative.image_type, video_duration=creative.video_duration, extra=creative.extra,
                         impr_monitor_url=creative.impr_monitor_url, click_monitor_url=creative.click_monitor_url,
                         deeplink=creative.deeplink, desc=creative.desc, status=creative.status)
    return creative_info


def advertiser_json(advertiser):
    """
    构建advertiser数据模型的json格式
    :param advertiser
    :return: dict
    """

    advertiser_info = dict(advertiser_name=advertiser.advertiser_name, site_name=advertiser.site_name,
                           url=advertiser.url, connector=advertiser.connector, phone=advertiser.phone,
                           email=advertiser.email, address=advertiser.address, brand=advertiser.brand,
                           category=advertiser.category, qualifications=advertiser.qualifications, qq=advertiser.qq,
                           province=advertiser.province, city=advertiser.city, advertiser_id=advertiser.advertiser_id)
    return advertiser_info


def get_json(emar_template):
    """
    构建emar_template数据模型的json格式
    :param emar_template
    :return: dict
    """
    temp_info = dict(template_id=emar_template.template_id, width_height=emar_template.width_height,
                     interview_mode=emar_template.interview_mode, picture_name=emar_template.picture_name,
                     picture_flag=emar_template.picture_flag, picture_code=emar_template.picture_code,
                     picture_width=emar_template.picture_width, picture_height=emar_template.picture_height,
                     picture_size=emar_template.picture_size, logo_name=emar_template.logo_name,
                     logo_flag=emar_template.logo_flag, logo_code=emar_template.logo_code,
                     logo_width=emar_template.logo_width, logo_height=emar_template.logo_height,
                     logo_size=emar_template.logo_size, title=emar_template.title, title_flag=emar_template.title_flag,
                     title_size=emar_template.title_size, description=emar_template.description,
                     description_flag=emar_template.description_flag, description_size=emar_template.description_size,
                     call_to_action=emar_template.call_to_action, call_to_action_flag=emar_template.call_to_action_flag,
                     call_to_action_size=emar_template.call_to_action_size, deeplink_url=emar_template.deeplink_url,
                     deeplink_url_flag=emar_template.deeplink_url_flag, landing_page=emar_template.landing_page,
                     landing_page_flag=emar_template.landing_page_flag, appid=emar_template.appid,
                     appid_flag=emar_template.appid_flag, package_name=emar_template.package_name,
                     package_name_flag=emar_template.package_name_flag)
    return temp_info
