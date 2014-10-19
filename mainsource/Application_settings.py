__author__ = 'lpj'
# -*- coding:utf8 -*-
import tornado
from mainsource import dbutils
from mainsource.config import config
class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = config.get_handers()
        settings = config.get_settings()
        tornado.web.Application.__init__(self, handlers, **settings)
        #mysql数据库
        self.mysql_db = dbutils.get_db()

        #sphinx
        self.sphinx_client = config.get_sphinxClient()






