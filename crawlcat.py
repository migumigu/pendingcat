#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding: utf-8

import pytumblr
import yaml
import os
import sys
#import urlparse
#import code
#import oauth2 as oauth
#from pandas import Series, DataFrame
#使用小熊猫库,做数据整理等
import pandas as pd
#自写函数导入
from blindcat import new_oauth, blind_sort

#主程序入口
if __name__ == '__main__':
    #此两行非常重要,由此来支持发送utf8中文内容
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #在conf(ig)目录下,设定配置文件,后续支持多个账户配置
    yaml_path = './conf/.tumblr'

    #如果配置文件不存在,则让用户输入访问tumblr API所必须的所有参数
    #如果存在,则读取配置文件数据
    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    #通过相关的配置信息,创建pytumblr客户端
    client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

    startpos = 0
    while True:
        followblogs = client.following(offset=startpos)
        df = pd.DataFrame(followblogs['blogs'])
        if len(df) is 0:
            break
        startpos += len(df)
        print df['name']

    #抓取某个指定博客的所有博客数据，并将其存入文件之中
    while True:
        name = raw_input("请输入博客名:(x:退出)\n")
        print('hello',name)
        if name is 'x':
            break
        startpos = 0
        isshowhead = True
        while True:
            posts = client.posts(name, offset=startpos)
            frame = pd.DataFrame(posts['posts'])
            postsnum = len(frame)
            print ('get:',postsnum,' sum:', startpos)
            if postsnum is 0:
                break
            frame.to_csv(name + '.csv', encoding='utf-8', mode='a', header=isshowhead)
            startpos += postsnum
            # 第一次把head给加上,后面批次的数据不需要加头
            isshowhead = False
        
    #创建一条中文文本博客a
#    zwtxt = 'Pending cat No.1 中文测试'
#    client.create_text("pendingcatno1", state="published", slug="testing-text-posts", title= unicode(zwtxt, "utf-8"), body="hello,tumblr!")

    #获取主页数据,并通过pandas对数据做抽取和表格化,展示获取到的数据
    #dashboard = client.dashboard()
    #frame = pd.DataFrame(dashboard['posts'],columns=['id','reblog_key','blog_name','type','liked','followed','is_nsfw','note_count','date','blog'])
    #print frame
    #dfsort = blind_sort(dashboard)
    #获取一个指定标量
    #print dfsort.loc[dfsort.index[0],'id']

    print ' --- end ---\n'


#    print 'pytumblr client created. You may run pytumblr commands prefixed with "client".\n'

#    code.interact(local=dict(globals(), **{'client': client}))
