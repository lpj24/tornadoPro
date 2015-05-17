__author__ = 'lpj'
#-*- coding:utf8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
from web_db import url_route
import sys


def main():
    print "server start"
    http_server = tornado.httpserver.HTTPServer(url_route.application)
    port = int(sys.argv[1].split('=')[1])
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
