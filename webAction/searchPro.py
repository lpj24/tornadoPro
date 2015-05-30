#-*- coding:utf8 -*-
import torndb
import tornado.web
import tornado.ioloop
import tornado.httpserver
from bs4 import BeautifulSoup  
import re,os,urllib2
import os.path
import time
#解决bs从抓取网页信息插入数据库时的编码问题
#start
from web_db import mysqlDB,sphinxDB
from multiprocessing import Pool
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf-8')


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("searchPage.html",queryset="",keyword="")

class QueryHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument("keyword",None)
        res =sphinxDB.get_sphinxClient().Query(keyword,'*')
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

            queryset = mysqlDB.get_db().query(sqlQuery,ids)
        else:
            pass

        logging.warn("DEBUG output arg:%ss",{"queryset":queryset,"keyword":keyword})
        self.render("searchPage.html",queryset=queryset,keyword=keyword)

class SyncHandler(tornado.web.RequestHandler):
        #get the dangdang's html
    def getTotal(self,dnsName):
        url = 'http://'+dnsName+'/pg1-cp01.54.06.00.00.00.html'
        html = urllib2.urlopen(urllib2.Request(url)).read()
        soup = BeautifulSoup(html,from_encoding="gb18030")
        totalString = soup.find_all('li',attrs={"class":"page_input"})[0].span.string
        totPage = int(re.findall(r"(\d+)",totalString)[0])
        return totPage

    def get(self):
        start_time = time.time()
        dnsName = 'category.dangdang.com'
        totPage = self.getTotal(dnsName)
        p = Pool(2)
        for i in xrange(totPage):
            p.apply_async(pushinMysql,args=(i,))
        p.close()
        p.join()
        print "数据同步时间",time.time()-start_time
        self.render("searchPage.html",queryset="",keyword="")

#抓取数据入库
mysql_db = mysqlDB.get_db()
def pushinMysql(i):
    dnsName = 'category.dangdang.com'
    url = "http://"+dnsName+"/pg"+str(i+1)+"-cp01.54.06.00.00.00.html"
    html = urllib2.urlopen(urllib2.Request(url)).read()
    soup = BeautifulSoup(html,from_encoding="gb18030")
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
        mysql_db.execute(sql,str(dic_source["title"]),str(dic_source["href"]),str(dic_source["alt"]),
                         str(dic_source["src"]),str(dic_source["detail"]))


