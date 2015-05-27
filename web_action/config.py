#-*- coding:utf8 -*-
import os
import os.path
from sphinxapi import *
import tornado
#获取配置文件,路由列表,数据库信息
class config:
    @classmethod
    def get(self,key):
        #s
        config_table = {}
        if not config_table:
            config_table = {
                "mysql_host":"127.0.0.1:3306",
                "mysql_database":"search",
                "mysql_user":"root",
                "mysql_password":"123"
            }

        return config_table.get(key)
