#-*-coding:utf8 -*-
import torndb
from config import config
import tornado.web
def get_db():
    db = None
    if not db:
        host = config.get("mysql_host")
        database = config.get("mysql_database")
        user = config.get("mysql_user")
        password = config.get("mysql_password")
        db = torndb.Connection(host,database,user,password)
    return db
