# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import config as cfg
import datetime
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import pymongo
from model import Bbasak
import threading

mongo_server = '35.167.123.242'
mongo = MongoClient(host=mongo_server, port=27017)
db = mongo.smartphone
db.bbasak.create_index("link")
# connection_string = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(cfg.DB_USER, cfg.DB_PWD, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_DB)
# engine = create_engine(connection_string, pool_recycle=3600, encoding='utf-8')
# Session = sessionmaker(bind=engine)

class BbasakDAO(object):
    def __init__(self):
        pass

    def save_posts(self, posts_id, date, title, content, type):
        # session = Session()
        if not self.get_posts_by_id(posts_id):
            print(date)
            db.bbasak.insert_one({'link': posts_id, 'date': date, 'title': title, 'content': content, 'crawl_time': datetime.datetime.now(), 'product' : type})

    def get_posts_by_id(self, posts_id):

        try:
            return db.bbasak.find_one({"link": posts_id})
        except Exception as e:
            print e


