#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time
import redis
import logging
import pymysql
import unittest
import traceback
from pymongo import MongoClient


class MongoDB(object):
    def __init__(self, host, port, db, table, user=None, password=None, only_index=None):
        self.mongo_host = host
        self.mongo_port = port
        self.mongo_user = user
        self.mongo_password = password
        self.mongo_db = db
        self.table = table
        self.only_index = only_index
        self.mongo_conn = None

    def connect(self):
        try:
            # 登陆认证
            if self.mongo_user is not None:
                client = MongoClient(self.mongo_host, self.mongo_port)
                db = client[self.mongo_db]
                db.authenticate(self.mongo_user, self.mongo_password)
            else:
                client = MongoClient(self.mongo_host, self.mongo_port)
                db = client[self.mongo_db]
            self.mongo_conn = db[self.table]
            # 添加唯一索引
            if self.only_index is not None:
                self.mongo_conn.ensure_index(self.only_index, unique=True)
            logging.info('connect to mongodb {0}'.format(self.mongo_conn))
        except Exception as err:
            logging.error('get_mongodb_conn connect error:{0}'.format(err))
            logging.error(traceback.format_exc())
            self.mongo_conn = None

    def insert(self, items):
        res = True
        try:
            if isinstance(items, dict):
                if 'update_time' not in items:
                    items['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                self.mongo_conn.insert_one(items)
            elif isinstance(items, list):
                items = [item.update({'update_time': time.strftime('%Y-%m-%d %H:%M:%S')}) for item in items
                         if 'update_time' not in item]
                self.mongo_conn.insert_many(items)
            else:
                logging.error("Only dictionaries or list are supported")
                res = False
        except Exception as err:
            logging.error('insert the info {0} to mongo failed {1}'.format(items, err))
            res = False
        return res

    def find(self, *args, **kwargs):
        res = None
        try:
            res = self.mongo_conn.find(*args, **kwargs)
        except Exception as e:
            logging.error(e)
        return res

    def get_count(self, key):
        res = ''
        try:
            res = self.mongo_conn.find(key).count()
        except Exception as e:
            print(e)
        return res

    def update(self, key_dic, update_dic):
        res = None
        try:
            update_dic['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            res = self.mongo_conn.update(key_dic, update_dic, True)
        except Exception as e:
            logging.error(e)
        return res


class DbMysql(object):
    def __init__(self, host, port, user, password, db):
        self.my_host = host
        self.my_port = port
        self.my_user = user
        self.my_password = password
        self.my_db = db
        self.my_conn = None
        self.connect()

    def connect(self):
        try:
            self.my_conn = pymysql.connect(host=self.my_host,
                                           user=self.my_user,
                                           passwd=self.my_password,
                                           port=self.my_port,
                                           db=self.my_db,
                                           charset="utf8")
            logging.info('connect to msyql {0}'.format(self.my_conn))
        except Exception as err:
            logging.error('get_mdb_conn connect error:{0}'.format(err))
            self.my_conn = None

    def execute(self, sqls):
        status_code = 0
        if not isinstance(sqls, list):
            sqls = [sqls]
        with self.my_conn.cursor() as cursor:
            i = 0
            retry = False
            while i < len(sqls):
                sql = sqls[i]
                try:
                    cursor.execute(sql)
                    logging.info(sql)
                except Exception as e:
                    if e.args[0] == 1062:
                        pass
                    elif e.args[0] == 2006 or e.args[0] == "(0, '')":
                        if not retry:
                            retry = True
                            self.connect()
                            # 重新连接 再次执行
                            continue
                        else:
                            status_code += -1
                    else:
                        logging.error(e)
                        logging.error(sql)
                        logging.error(traceback.format_exc())
                        status_code += -1
                i += 1
                if retry:
                    retry = False
        return status_code

    def query(self, sql):
        rows = []
        with self.my_conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
            except Exception as e:
                if e.args[0] != '(0, \'\')':
                    logging.error(e)
                    logging.error(sql)
                    logging.error(traceback.format_exc())
        return rows

    def commit(self):
        self.my_conn.commit()

    def close(self):
        self.my_conn.close()


class Rds(object):
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.rds = None

    def connect_rds(self):
        try:
            self.rds = redis.Redis(host=self.host,
                                   port=self.port,
                                   db=self.db,
                                   password=self.password,
                                   decode_responses=True)
            logging.info('redis host[{0}] port[{1}]'.format(self.host, self.port))
        except Exception as err:
            logging.error('get_rds_conn connect error:{0}'.format(err))
            self.rds = None
            sys.exit(-1)

    def rds_hget(self, store_hash, store_field):
        res = None
        try:
            res = self.rds.hget(store_hash, store_field)
        except Exception as e:
            logging.error(e)
        return res

    def rds_hset(self, store_hash, store_field, store_items):
        res = None
        try:
            res = self.rds.hset(store_hash, store_field, store_items)
        except Exception as err:
            logging.error(err)
        return res

    def rds_hincr(self, name, key, amount=1):
        res = None
        try:
            res = self.rds.hincrby(name, key, amount)
            print("ds", res)
        except Exception as err:
            logging.error(err)
        return res

    def rds_hexists(self, name, key):
        res = None
        try:
            res = self.rds.hexists(name, key)
        except Exception as err:
            logging.error(err)
        return res

    def rds_len(self, name):
        res = None
        try:
            res = self.rds.llen(name)
        except Exception as err:
            logging.error(err)
        return res

    def rds_hkey(self, name):
        res = None
        try:
            res = self.rds.hkeys(name)
        except Exception as e:
            logging.error(e)
        return res

    def rds_hdel(self, filed, key):
        res = None
        try:
            res = self.rds.delete(filed, key)
        except Exception as e:
            logging.error(e)
        return res


class TestMongo(unittest.TestCase):
    def test_init(self):
        mdb = MongoDB(host='127.0.0.1', port=27017, user='maimeng', password='maimeng', db='maimeng',
                      table='test_table')
        mdb.connect()
        mydict = {"creative_id": '001', "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"}
        mylist = [
            {"creative_id": '002', "name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
            {"creative_id": '003', "name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
            {"creative_id": '004', "name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
            {"creative_id": '005', "name": "Github", "alexa": "109", "url": "https://www.github.com"}
        ]
        # # 插入一条
        # res = mdb.insert(mydict)
        # print('插入一条的结果为 {0}'.format(res))
        # # 插入多条
        # res1 = mdb.insert(mylist)
        # print('插入多条的结果为 {0}'.format(res1))


        # 查询全部
        results = mdb.get_count({'creative_id': '00'})
        print(results)
        # for result in results:
        #     mdb.update({'creative_id': '002'}, result)
        #
        # results = mdb.find({'creative_id': '002'})
        # for result in results:
        #     print(result)

if __name__ == '__main__':
    unittest.main()
