# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import config as cfg
import datetime
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from model import Dcinside

connection_string = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(cfg.DB_USER, cfg.DB_PWD, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_DB)
engine = create_engine(connection_string, pool_recycle=3600, encoding='utf-8')
Session = sessionmaker(bind=engine)

class DcDAO(object):
    def __init__(self):
        pass

    def save_posts(self, posts_id, date, title, content, read):
        session = Session()
        if not self.get_posts_by_id(posts_id):
            posts = Dcinside(link=posts_id, date=date, title=title, content=content, read_no=read, crawl_time=datetime.datetime.now())
            session.add(posts)
            session.commit()
        session.close()

    def get_posts_by_id(self, posts_id):
        try:
            session = Session()
            row = session.query(Dcinside).filter(Dcinside.link == posts_id).first()
            return row
        except Exception as e:
            print e
        finally:
            session.close()


