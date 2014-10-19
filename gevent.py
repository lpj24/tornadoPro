import tornado.wsgi
import gevent.wsgi

import searchPro


application = tornado.wsgi.WSGIApplication([
(r"/", searchPro.HomeHandler),
], searchPro.Application().settings)

if __name__ == "__main__":
	server = gevent.pywsgi.WSGIServer(('', 8888), application)
	server.serve_forever()