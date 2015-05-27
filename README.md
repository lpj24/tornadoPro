tornadoPro
sphinx全文检索由django迁移到tornado上,使用多进程并行抓取

使用beautifulsoup从当当网抓取所有的程序设计类书籍存储到mysql数据库，用croeseek做全文索引，tornado
supervisord为tornado做守护进程  使用upstart对nginx和coreseek进行管理

1.首先从当当网抓取程序设计类书籍。见syncHandler类，获取当当网的程序设计类书籍的总页数,遍历总页数获取所有的书籍，获取书籍的图片，标题，链接，alt,详细概述。插入到mysql书籍库

2.更新sphinx的索引，启动sphinx的进程,首先ps -eo comm,cmd,pid | grep searchd查处sphinx的进程pid，kill -QUIT searched的pid号 然后./indexer --all启动所有的索引,./searchd启动进程

3.查询是queryHandler类。使用sphinxapi模块，操作详解http://6167018.blog.51cto.com/6157018/1435150我的博客



使用nginx反向代理，配置文件见nginx.conf。tornado进程不是Demon进程，当终端关闭等情况，则进程停止，tornado服务不能访问，supervisord管理进程在/etc/supervisord/supervisord.conf添加要守护的进程
