#-*- coding:utf8 -*-
import os
import os.path
import searchPro
from sphinxapi import *
import tornado
#获取配置文件,路由列表,数据库信息
class config:
    @classmethod
    def get(self,key):
        config_table = {}
        if not config_table:
            config_table = {
                "mysql_port":8888,
                "mysql_host":"127.0.0.1:3306",
                "mysql_database":"search",
                "mysql_user":"root",
                "mysql_password":"123"
            }

        return config_table.get(key)

    @classmethod
    def get_settings(self):
        settings_table = {}
        if not settings_table:
            settings_table = {
                "blog_title":"search sphinx",
                "template_path":os.path.join("/home/lpj/tornadoPro", "templates"),
                "static_path":os.path.join("/home/lpj/tornadoPro", "static"),
                #ui_modules={"Entry": EntryModule},
                "xsrf_cookies":True,
                #cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                #login_url="/auth/login",
                "gzip":True,
                "debug":False,

            }

        return settings_table


    @classmethod
    def get_handers(self):
        handers_table = {}
        if not handers_table:
            handers_table = [
                (r'/', searchPro.HomeHandler),
                (r'/query/*', searchPro.QueryHandler),
                (r'/updateDB/', searchPro.SyncHandler),

            ]

        return handers_table

    @classmethod
    def get_sphinxClient(self):
        client = None
        if not client:
            client = SphinxClient()
            client.SetServer('localhost',9312)
            client.SetMatchMode(SPH_MATCH_ANY)
        return client



class BaseHandler(tornado.web.RequestHandler):
    @property
    def mysl_db(self):
        return self.application.mysql_db

    @property
    def sphinx_db(self):
        return self.application.sphinx_client