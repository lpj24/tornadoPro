#-*- coding:utf8 -*-
import torndb
import tornado.web
import tornado.ioloop
import tornado.httpserver
from sphinxapi import *
from bs4 import BeautifulSoup  
import re,os,urllib2
from mainsource.config import config
import os.path
from mainsource.config import BaseHandler

#解决bs从抓取网页信息插入数据库时的编码问题
#start
import sys
reload(sys)
sys.setdefaultencoding('utf-8')






class HomeHandler(BaseHandler):
    def get(self):
        self.render("searchPage.html",queryset="",keyword="")

class QueryHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        keyword = self.get_argument("keyword",None)
        res = self.sphinx_db.Query(keyword,'*')
        listid = []
        ids = ()
        queryset = {}
        if len(res['matches']) > 0:
            listid = [i['id'] for i in res['matches']]
            ids = tuple(listid)
            if len(ids) == 1:
                ids = ids[0]
                sqlQuery = "select id,title,href,alt,imgsrc,detail from designBook where id=%s"
            else:
                sqlQuery = "select id,title,href,alt,imgsrc,detail from designBook where id in %s"

            queryset = self.mysl_db.query(sqlQuery,ids)
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

    @tornado.web.asynchronous
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
            

           
            for index,text in enumerate(source):
                sql = "insert into designBook (title,href,alt,imgsrc,detail) values (%s,%s,%s,%s,%s)"
                dic_source = {}
                dic_source["title"] = text.get("title")
                dic_source["href"] = text.get("href")
                dic_source["alt"] = text.find('img').get('alt')
                dic_source["src"] = text.find('img').get('src')
                dic_source["detail"] = sourceDetial[index].string
                self.mysl_db.execute(sql,str(dic_source["title"]),str(dic_source["href"]),str(dic_source["alt"]),str(dic_source["src"]),str(dic_source["detail"]))
                list.append(dic_source)

        self.render("searchPage.html",queryset="")




