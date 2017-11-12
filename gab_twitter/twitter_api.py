''' twitter_api.py
This is a work in progress

Example:
>> tw = twitter_connect(TWITTER_API_KEYS)
>> get_follower_descriptions('username', tw)
{
...
	screen_name: profile_description,
...
}
'''

import time
import tweepy

from credentials import TWITTER_API_KEYS

_target_screen_name = 'breitbartnews'  # ~75k followers

def twitter_connect(twitter_creds):
    auth = tweepy.OAuthHandler(
        twitter_creds['consumer_key'],
        twitter_creds['consumer_secret'])
    auth.set_access_token(
        twitter_creds['access_token_key'],
        twitter_creds['access_token_secret'])
    tw = tweepy.API(auth)
    return tw

# from http://docs.tweepy.org/en/v3.5.0/code_snippet.html#handling-the-rate-limit-using-cursors
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print 'sleeping...'
            time.sleep(15 * 60)

def get_follower_descriptions(scrn_name, api):
    '''
    input: screen_name
    output: {screen_name: profile_description}
        - screen names and profile bio/description of all followers for input screen_name
    '''
    followers = {}
    # use .pages() instead of .items()?
    # works on small number of followers without the limit_handled wrapper
    for follower in limit_handled(tweepy.Cursor(api.followers, screen_name=_target_screen_name).items()):
        k = follower.screen_name
        v = follower.description
        print 'adding {}'.format(k)
        followers[k] = v
    return followers
