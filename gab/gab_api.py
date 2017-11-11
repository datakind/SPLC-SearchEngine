'''gab_api.py
We can get posts from users and search but we cannot get following/followers easily.
Maybe something like Selenium would do the trick with that

Some not-so-useful info here: https://gab.ai/docs

Example: 
# > s = start_session(login_payload)
# > user = get_user_feed(USER, s)
# > srch = search('Coulter',s)
'''

import json
from pprint import pprint
import re
import requests as req
import sys

LOGIN_URL = 'https://gab.ai/auth/login'
USER = 'a'
HEADERS = {}
HIDDEN_TOKEN_RE = '<input type="hidden" name="_token" value="(.*)">'

# fake name: Brandon E. Pike
login_payload = {
    'username': 'regseorg@gjnwrg.com',  # or brandon_e_pike
    'password': 'fakeaccount',
    'remember': True
}

def start_session(login_info):
    s = req.Session()
    resp = s.get(LOGIN_URL)
    login_info['XSRF-TOKEN'] = s.cookies['XSRF-TOKEN']
    login_info['laravel_session'] = s.cookies['laravel_session']
    login_info['__cfduid'] = s.cookies['__cfduid']
    _token = re.findall(HIDDEN_TOKEN_RE, resp.text)
    login_info['_token'] = _token
    p = s.post(LOGIN_URL, data=login_info)
    return s

def get_user_feed(user_name, session):
    '''input user_name and session
    return dict of feed (possibly limited to latest 28 posts per gab: @docs)
    - todo: output into a dataframe with relevant columns from json
    '''
    url = 'https://gab.ai/feed/{usr}'.format(usr=user_name)
    user = session.get(url)
    return user.json()

def search(query, session, sort='relevance'):
    '''Available sort keys: date, relevance, score
    Returns dictionary of results
    '''
    if sort not in ('date', 'relevance', 'score'):
        sys.exit('Sort key must be one of: date, relevance, score')
    url = 'https://gab.ai/api/search?sort={srt}&q={qry}'.format(srt=sort, qry=query)
    print url
    results = session.get(url)
    return results.json()

def get_referenced_users(feed):
    ''' input feed dictionary
    - Search for other mentions within that feed like @<username>
    - Mentions can be source of retweets, replies, mentions in body of 
        posts, etc...

    '''
    pass

def feed_contains_taget_urls(feed, target_url_list):
    pass
