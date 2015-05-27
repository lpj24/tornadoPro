import os

import tornado.web

from webAction.searchPro import *

settings = {
    "debug":True,
    "template_path":os.path.join("/home/lpj/tornadoPro","templates"),
    "static_path":os.path.join("/home/lpj/tornadoPro","static"),
    "xsrf_cookies":True,
    "gzip":True
}
application = tornado.web.Application([
    (r"/",HomeHandler),
    (r"/query/*",QueryHandler),
    (r"/updateDB",SyncHandler)


],**settings)
~               
