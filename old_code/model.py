# -*- coding :utf-8 -*-

import os
import sys
from sqlalchemy import Column, String, Integer, CHAR, Date, ForeignKey, Time, Index, DateTime, TIMESTAMP, func
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dcinside(Base):
    __tablename__ = 'dcinside'

    link            = Column(String(300), primary_key=True, nullable=False)
    date            = Column(DateTime, nullable=False)
    title           = Column(String(200), nullable=False)
    content         = Column(TEXT, nullable=False)
    read_no         = Column(String(10), nullable=False)
    crawl_time      = Column(DateTime, nullable=False)

class Bbasak(Base):
    __tablename__ = 'bbasak'

    link            = Column(String(300), primary_key=True, nullable=False)
    date            = Column(DateTime, nullable=False)
    title           = Column(String(200), nullable=False)
    content         = Column(TEXT, nullable=False)
    read_no         = Column(String(10), nullable=False)
    crawl_time      = Column(DateTime, nullable=False)
