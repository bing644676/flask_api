#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from emar_config import *

# 数据库相关变量声明
engine_info = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                                        MYSQL_PORT, MYSQL_DB)
engine = sqlalchemy.create_engine(engine_info, echo=False, convert_unicode=True)
BaseModel = sqlalchemy.ext.declarative.declarative_base()


# 构建数据模型crowd
class Crowd(BaseModel):
    __tablename__ = "crowd"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    crowd_id = sqlalchemy.Column("crowd_id", sqlalchemy.Integer, nullable=False)
    crowd_name = sqlalchemy.Column("crowd_name", sqlalchemy.String(50), nullable=False)
    status = sqlalchemy.Column("status", sqlalchemy.Integer, default=1)


# 构建数据模型Channel
class Channel(BaseModel):
    __tablename__ = "channel"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    channel_id = sqlalchemy.Column("channel_id", sqlalchemy.Integer, nullable=False)
    channel_name = sqlalchemy.Column("channel_name", sqlalchemy.String(50), nullable=False)
    status = sqlalchemy.Column("status", sqlalchemy.Integer, nullable=True)


# 构建数据模型campaign
class Campaign(BaseModel):
    __tablename__ = "campaign"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    advertiser_id = sqlalchemy.Column("advertiser_id", sqlalchemy.Integer, nullable=False)
    creative_name = sqlalchemy.Column("creative_name", sqlalchemy.String(50), nullable=False)
    category = sqlalchemy.Column("category", sqlalchemy.Integer, nullable=False)
    platform = sqlalchemy.Column("platform", sqlalchemy.Integer, nullable=False)
    budget = sqlalchemy.Column("budget", sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column("price", sqlalchemy.Float, nullable=False)
    status = sqlalchemy.Column("status", sqlalchemy.Integer, nullable=False)
    adx_ids = sqlalchemy.Column("adx_ids", sqlalchemy.String(200), nullable=False)
    speed = sqlalchemy.Column("speed", sqlalchemy.Integer, nullable=False)
    start_date = sqlalchemy.Column("start_date", sqlalchemy.String(50), nullable=True)
    end_date = sqlalchemy.Column("end_date", sqlalchemy.String(50), nullable=True)
    week_hours = sqlalchemy.Column("week_hours", sqlalchemy.String(500), nullable=True)
    areas = sqlalchemy.Column("areas", sqlalchemy.String(200), nullable=True)
    ip_list = sqlalchemy.Column("ip_list", sqlalchemy.String(200), nullable=True)
    device_brand = sqlalchemy.Column("device_brand", sqlalchemy.String(200), nullable=True)
    device_price = sqlalchemy.Column("device_price", sqlalchemy.String(200), nullable=True)
    connection = sqlalchemy.Column("connection", sqlalchemy.String(200), nullable=True)
    os = sqlalchemy.Column("os", sqlalchemy.String(200), nullable=True)
    lbs = sqlalchemy.Column("lbs", sqlalchemy.String(200), nullable=True)
    crowds = sqlalchemy.Column("crowds", sqlalchemy.String(200), nullable=True)
    creatives = sqlalchemy.Column("creatives", sqlalchemy.String(200), nullable=False)


# 构建数据模型creative
class Creative(BaseModel):
    __tablename__ = "creative"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    advertiser_id = sqlalchemy.Column("advertiser_id", sqlalchemy.String(20), nullable=False)
    creative_id = sqlalchemy.Column("creative_id", sqlalchemy.String(20), nullable=True)
    creative_name = sqlalchemy.Column("creative_name", sqlalchemy.String(50), nullable=False)
    creative_type = sqlalchemy.Column("creative_type", sqlalchemy.Integer, nullable=False)
    creative_url = sqlalchemy.Column("creative_url", sqlalchemy.String(200), nullable=True)
    width = sqlalchemy.Column("width", sqlalchemy.Integer, nullable=False)
    height = sqlalchemy.Column("height", sqlalchemy.Integer, nullable=False)
    url = sqlalchemy.Column("url", sqlalchemy.String(200), nullable=False)
    size = sqlalchemy.Column("size", sqlalchemy.Integer, nullable=True)
    landing_page = sqlalchemy.Column("landing_page", sqlalchemy.String(200), nullable=False)
    title = sqlalchemy.Column("title", sqlalchemy.String(50), nullable=True)
    image_type = sqlalchemy.Column("image_type", sqlalchemy.Integer, nullable=True)
    video_duration = sqlalchemy.Column("video_duration", sqlalchemy.Integer, nullable=True)
    extra = sqlalchemy.Column("extra", sqlalchemy.String(200), nullable=True)
    impr_monitor_url = sqlalchemy.Column("impr_monitor_url", sqlalchemy.String(200), nullable=True)
    click_monitor_url = sqlalchemy.Column("click_monitor_url", sqlalchemy.String(200), nullable=True)
    deeplink = sqlalchemy.Column("deeplink", sqlalchemy.String(200), nullable=True)
    desc = sqlalchemy.Column("desc", sqlalchemy.String(50), nullable=True)
    status = sqlalchemy.Column("status", sqlalchemy.Integer, nullable=False)


# 构建数据模型Advertiser
class Advertiser(BaseModel):
    __tablename__ = "advertiser"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    advertiser_name = sqlalchemy.Column("advertiser_name", sqlalchemy.String(20), nullable=False)
    site_name = sqlalchemy.Column("site_name", sqlalchemy.String(100), nullable=False)
    url = sqlalchemy.Column("url", sqlalchemy.String(200), nullable=False)
    connector = sqlalchemy.Column("connector", sqlalchemy.String(20), nullable=False)
    phone = sqlalchemy.Column("phone", sqlalchemy.String(20), nullable=False)
    email = sqlalchemy.Column("email", sqlalchemy.String(50), nullable=True)
    address = sqlalchemy.Column("address", sqlalchemy.String(100), nullable=True)
    brand = sqlalchemy.Column("brand", sqlalchemy.String(100), nullable=True)
    category = sqlalchemy.Column("category", sqlalchemy.Integer, nullable=False)
    qualifications = sqlalchemy.Column("qualifications", sqlalchemy.String(500), nullable=False)
    qq = sqlalchemy.Column("qq", sqlalchemy.String(20), nullable=True)
    province = sqlalchemy.Column("province", sqlalchemy.String(20), nullable=True)
    city = sqlalchemy.Column("city", sqlalchemy.String(20), nullable=True)
    advertiser_id = sqlalchemy.Column("advertiser_id", sqlalchemy.String(20), nullable=True)


# 构建数据模型EmarTemplate
class EmarTemplate(BaseModel):
    __tablename__ = "emar_template"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }

    # EmarTemplate表结构
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    template_id = sqlalchemy.Column("template_id", sqlalchemy.Integer, nullable=False)
    width_height = sqlalchemy.Column("width_height", sqlalchemy.String(50), nullable=True)
    interview_mode = sqlalchemy.Column("interview_mode", sqlalchemy.String(50), nullable=True)

    picture_name = sqlalchemy.Column("picture_name", sqlalchemy.String(50), nullable=True)
    picture_flag = sqlalchemy.Column("picture_flag", sqlalchemy.String(50), nullable=True)
    picture_code = sqlalchemy.Column("picture_code", sqlalchemy.String(50), nullable=True)
    picture_width = sqlalchemy.Column("picture_width", sqlalchemy.Integer, nullable=False)
    picture_height = sqlalchemy.Column("picture_height", sqlalchemy.Integer, nullable=False)
    picture_size = sqlalchemy.Column("picture_size", sqlalchemy.Integer, nullable=False)

    logo_name = sqlalchemy.Column("logo_name", sqlalchemy.String(50), nullable=True)
    logo_flag = sqlalchemy.Column("logo_flag", sqlalchemy.String(50), nullable=True)
    logo_code = sqlalchemy.Column("logo_code", sqlalchemy.String(50), nullable=True)
    logo_width = sqlalchemy.Column("logo_width", sqlalchemy.Integer, nullable=False)
    logo_height = sqlalchemy.Column("logo_height", sqlalchemy.Integer, nullable=False)
    logo_size = sqlalchemy.Column("logo_size", sqlalchemy.Integer, nullable=False)

    title = sqlalchemy.Column("title", sqlalchemy.String(50), nullable=True)
    title_flag = sqlalchemy.Column("title_flag", sqlalchemy.String(50), nullable=True)
    title_size = sqlalchemy.Column("title_size", sqlalchemy.String(50), nullable=True)

    description = sqlalchemy.Column("description", sqlalchemy.String(50), nullable=True)
    description_flag = sqlalchemy.Column("description_flag", sqlalchemy.String(50), nullable=True)
    description_size = sqlalchemy.Column("description_size", sqlalchemy.String(50), nullable=True)

    call_to_action = sqlalchemy.Column("call_to_action", sqlalchemy.String(50), nullable=True)
    call_to_action_flag = sqlalchemy.Column("call_to_action_flag", sqlalchemy.String(50), nullable=True)
    call_to_action_size = sqlalchemy.Column("call_to_action_size", sqlalchemy.String(50), nullable=True)

    deeplink_url = sqlalchemy.Column("deeplink_url", sqlalchemy.String(50), nullable=True)
    deeplink_url_flag = sqlalchemy.Column("deeplink_url_flag", sqlalchemy.String(50), nullable=True)

    landing_page = sqlalchemy.Column("landing_page", sqlalchemy.String(50), nullable=True)
    landing_page_flag = sqlalchemy.Column("landing_page_flag", sqlalchemy.String(50), nullable=True)

    appid = sqlalchemy.Column("appid", sqlalchemy.String(50), nullable=True)
    appid_flag = sqlalchemy.Column("appid_flag", sqlalchemy.String(50), nullable=True)

    package_name = sqlalchemy.Column("package_name", sqlalchemy.String(50), nullable=True)
    package_name_flag = sqlalchemy.Column("package_name_flag", sqlalchemy.String(50), nullable=True)


# 利用Session对象连接数据库
DBSessinon = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSessinon()
# 创建所有表,如果表已经存在,则不会创建
BaseModel.metadata.create_all(engine)
