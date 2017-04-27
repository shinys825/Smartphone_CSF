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
from model import Dcinside

mongo_server = 'ec2-35-167-123-242.us-west-2.compute.amazonaws.com'
mongo = MongoClient(mongo_server, 27017)
db = mongo.smartphone
db.bbasak.create_index("link")
# connection_string = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(cfg.DB_USER, cfg.DB_PWD, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_DB)
# engine = create_engine(connection_string, pool_recycle=3600, encoding='utf-8')
# Session = sessionmaker(bind=engine)

class DcDAO(object):
    def __init__(self):
        pass

    def save_posts(self, posts_id, date, title, content, type):
        #session = Session()
        if not self.get_posts_by_id(posts_id):
            print(date)
            db.dcinside.insert_one({'link': posts_id, 'date': date, 'title': title, 'content': content, 'crawl_time': datetime.datetime.now(), 'product':type})

            #     posts = Dcinside(link=posts_id, date=date, title=title, content=content, crawl_time=datetime.datetime.now())
        #     session.add(posts)
        #     session.commit()
        # session.close()

    def get_posts_by_id(self, posts_id):
        try:
            # session = Session()
            # row = session.query(Dcinside).filter(Dcinside.link == posts_id).first()
            return db.dcinside.find_one({'link': posts_id})
        except Exception as e:
            print e



