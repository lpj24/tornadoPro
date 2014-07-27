#-*- coding:utf8 -*-
import torndb
import tornado.web
import tornado.ioloop
import tornado.httpserver
from sphinxapi import *
from bs4 import BeautifulSoup  
import re,os,urllib2
import os.path
from tornado.options import define,options

#解决bs从抓取网页信息插入数据库时的编码问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

define("port", default=8888, help="tornado port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="host")
define("mysql_database", default="search", help="database name")
define("mysql_user", default="root", help="user")
define("mysql_password", default="123", help="password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/query/*', QueryHandler),
            (r'/updateDB/', SyncHandler),
        ]
        settings = dict(
            blog_title="search sphinx",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            #cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            #login_url="/auth/login",
            gzip=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        #db 
        self.db = torndb.Connection(
        host=options.mysql_host, database=options.mysql_database,
        user=options.mysql_user, password=options.mysql_password)



class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db



class HomeHandler(BaseHandler):
    def get(self):
        self.render("searchPage.html",queryset="",keyword="")

class QueryHandler(BaseHandler):
    def get(self):
        keyword = self.get_argument("keyword",None)
        
        cl = SphinxClient()    
        cl.SetServer('localhost',9312)  
        #cl.SetWeights ( [100, 1] )
        cl.SetMatchMode(SPH_MATCH_ANY) 
        res = cl.Query(keyword,'*')
        listid = []
        ids = ()
        queryset = {}
        if len(res['matches']) > 0:
            for i in res['matches']:
                listid.append(i['id'])
            ids = tuple(listid)
            if len(ids) == 1:
                ids = ids[0]
                sqlQuery = "select id,title,href,alt,imgsrc,detail from designBook where id=%s"
            else:
                sqlQuery = "select id,title,href,alt,imgsrc,detail from designBook where id in %s"

            queryset = self.db.query(sqlQuery,ids)
        else:
            pass

        
        self.render("searchPage.html",queryset=queryset,keyword=keyword)

class SyncHandler(BaseHandler):
        #get the dangdang's html 
    def getTotal(self):
        proxy_handler = urllib2.ProxyHandler({'http': 'http://'+'58.68.246.12:18080'})      
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        url = 'http://category.dangdang.com/pg1-cp01.54.06.00.00.00.html'
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html,fromEncoding="gb18030")
        totalString = soup.find_all('li',attrs={"class":"page_input"})[0].span.string
        totPage = int(re.findall(r"(\d+)",totalString)[0])
        return totPage

    def get(self):
        #get total page count
        totPage = self.getTotal()
        proxy_handler = urllib2.ProxyHandler({'http': 'http://'+'58.68.246.12:18080'})      
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

        for i in xrange(totPage):
            url = "http://category.dangdang.com/pg"+str(i+1)+"-cp01.54.06.00.00.00.html"
            html = urllib2.urlopen(url).read()

            list = []
            soup = BeautifulSoup(html,fromEncoding="gb18030")
            source = soup.find_all('a',attrs={"class":"pic"})
            sourceDetial = soup.find_all('p',attrs={"class":"detail"})
            

           
            for item in xrange(len(source)):
                sql = "insert into designBook (title,href,alt,imgsrc,detail) values (%s,%s,%s,%s,%s)"
                dic_source = {}
                dic_source["title"] = source[item].get("title")
                dic_source["href"] = source[item].get("href")
                dic_source["alt"] = source[item].find('img').get('alt')
                dic_source["src"] = source[item].find('img').get('src')
                dic_source["detail"] = sourceDetial[item].string
                self.db.execute(sql,str(dic_source["title"]),str(dic_source["href"]),str(dic_source["alt"]),str(dic_source["src"]),str(dic_source["detail"]))
                list.append(dic_source)

        self.render("searchPage.html",queryset="")


def main():
    print "server start"
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop) 
    loop.start()

if __name__ == "__main__":
    main()
