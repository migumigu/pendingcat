# -*- coding: utf-8 -*-

import yaml
import oauth2 as oauth
import urlparse
import pandas as pd
from pandas import Series, DataFrame

#此函数用于创建配置文件时,读取用户输入的关键key,并将key存入指定的配置文件中
def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print 'Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps'
    consumer_key = raw_input('Paste the consumer key here: ')
    consumer_secret = raw_input('Paste the consumer secret here: ')

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)
 
    # Get request token
    resp, content = client.request(request_token_url, "POST")
    request_token =  urlparse.parse_qs(content)

    # Redirect to authentication page
    print '\nPlease go here and authorize:\n%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'][0])
    redirect_response = raw_input('Allow then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    url = urlparse.urlparse(redirect_response)
    query_dict = urlparse.parse_qs(url.query)
    oauth_verifier = query_dict['oauth_verifier'][0]

    # Request access token
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'][0])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = urlparse.parse_qs(content)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': access_token['oauth_token'][0],
        'oauth_token_secret': access_token['oauth_token_secret'][0]
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(tokens, yaml_file, indent=2)
    yaml_file.close()

    return tokens

#对DataFrame数据按一系列规则做排序,返回推荐的结果.不智能的瞎子排序
def blind_sort(dt):
    print type(dt)
    df = pd.DataFrame(dt['posts'],columns=['id','reblog_key','blog_name','type','can_like','liked','followed','is_nsfw','note_count','date','blog'])
    #打印入参类型,打印df内容
    print type(df)
    df = df[df['can_like'] == True]
    #print df
    #sort带key,升降序
    dfsort = df.sort(['note_count','is_nsfw'],ascending=[False,True])
    print dfsort
    return dfsort