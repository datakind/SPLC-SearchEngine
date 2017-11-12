'''gab_api.py

Util wrapper to grab data from grab.ai
Some not-so-useful info here: https://gab.ai/docs

We can get posts from users and search but we cannot get 
following/followers easily. Maybe something like Selenium would 
to have it intereactively pull data from the html.


Example: 
# > s = start_session(login_payload)
# > user = get_user_feed(USER, s)
# > srch = search('Coulter',s)

TODO: Add error handling + retires decoratos
'''

import json
from pprint import pprint
import re
import requests as req
import sys

from credentials import login_payload
import utils

LOGIN_URL = 'https://gab.ai/auth/login'
USER = 'a'
HEADERS = {}
HIDDEN_TOKEN_RE = '<input type="hidden" name="_token" value="(.*)">'


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

def get_user_feed(user_name, session, raw_posts=False, write_path=None):
    '''input user_name and session
    
    - return pandas df of feed (possibly limited to 28 posts per gab: @docs)
    - Option to return raw dictiory response with raw_posts flag
    - Dataframe does not include pinned post, raw data does
    - can output to a csv if write_path is specified
    '''
    url = 'https://gab.ai/feed/{usr}'.format(usr=user_name)
    response = session.get(url)
    user_posts = response.json()
    if raw_posts:
        return user_posts
    else:
        data = utils.make_dataframe_from_posts(user_posts['data'])
        if write_path:
            write_file = write_path + '{}_posts.csv'.format(user_name)
            data.to_csv(write_file, index=False, encoding='utf-8')
        return data

def search(query, session, sort='relevance'):
    '''Available sort keys: date, relevance, score
    Returns dictionary of results
    '''
    if sort not in ('date', 'relevance', 'score'):
        sys.exit('Sort key must be one of: date, relevance, score')
    url = 'https://gab.ai/api/search?sort={srt}&q={qry}'.format(srt=sort, qry=query)
    results = session.get(url)
    return results.json()

# TODO
def get_referenced_users(feed):
    ''' input feed dictionary
    - Search for other mentions within that feed like @<username>
    - Mentions can be source of retweets, replies, mentions in body of 
        posts, etc...

    '''
    pass

# TODO
def feed_contains_taget_urls(feed, target_url_list):
    pass
