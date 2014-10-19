__author__ = 'lpj'
#-*- coding:utf8 -*-
import searchPro
from mainsource.Application_settings import MyApplication
from mainsource.config import config
import tornado.web
import tornado.ioloop
import tornado.httpserver



def main():
    print "server start"
    http_server = tornado.httpserver.HTTPServer(MyApplication())
    print http_server.listen.im_class
    #app = Application()
    #app.listen(options.port)   web.application.listen be used to avoid the need to create httpserver
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()