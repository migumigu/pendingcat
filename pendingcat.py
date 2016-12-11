#!/usr/bin/python
#coding=utf-8

import pytumblr
import yaml
import os
import urlparse
import code
import oauth2 as oauth
from pandas import Series, DataFrame
import pandas as pd

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

if __name__ == '__main__':
    yaml_path = './conf/.tumblr'

    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

#    client.create_text("pendingcatno1", state="published", slug="testing-text-posts", title=u"Pending cat No.1 中文测试", body=u"hello,tumblr!你好")
    
    dashboard = client.dashboard()
    frame = pd.DataFrame(dashboard['posts'],columns=['id','blog_name','type','liked','followed','is_nsfw','note_count'])
    print frame
#    client.reblog("pendingcatno1", id='154075088261',reblog_key='tXqT68wR', comment="so cute, i love it.")
#    print frame['id'],frame['blog_name'],frame['type'],frame['header_focus_height'],frame['header_focus_width']
    
    print ' --- end ---\n'
"""    for pd in dashboard['posts']:
        blog = pd['blog']
        print 'blogname:' + pd['blog_name'] 
        print('id:',pd['id'])
        print 'type:' + pd['type'] 
        print blog['theme']['header_image'] +'\n'
"""

#    pd.DataFrame(dashboard)
    #print frame

#    print 'pytumblr client created. You may run pytumblr commands prefixed with "client".\n'

#    code.interact(local=dict(globals(), **{'client': client}))
