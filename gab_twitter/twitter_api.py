''' twitter_api.py

This will take a very long time for accounts with large amounts of followers bc
of twitter's api rate control limits.
'''

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
    tw = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return tw

def get_followers(api, scrn_name, output_dict_key='screen_name',user_fields=[]):
    '''
    input: screen_name
    output: dictionary with keys as output_dict_key (screen_name as default). 
    		Values can either be tweepy user objects or dictionary of specified 
    		user attributes passed in user_fields kwarg.
    Reference: 
    	https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

    Dummy Example:
        > breitbart_followers = get_followers('breitbartnews')
        > breitbart_followers['breitbartfan123'].description
          'Blah blah blah... Find me on gab.ai/breitbartfan123...'
    OR
        > breitbart_followers = get_followers('breitbartnews', user_field=['lang', 'description'])
        > breitbart_followers['breitbartfan123']
          {lang:'eng', description:'Blah blah blah... Find me on gab.ai/breitbartfan123...'}
    '''
    output_dict = {}
    for followers in tweepy.Cursor(api.followers, screen_name=scrn_name).pages():
        for usr in followers:
            k = usr.screen_name
            if not user_fields:
                # set the value to tweepy.models.User with all info
                v = usr
            else:
                try:
                    # set the value to dictionary of the given user fields
                    v = {user_field: usr._json[user_field] for user_field in user_fields}
                except KeyError, e:
                    sys.exit('KeyError: Invalid user attribute(s): {}'.format(user_fields))
                    
            output_dict[k] = v
    return output_dict

def get_tweets(screen_name, n, args):
	'''get n tweets from given user. Should be easy tweepy implementation'''
	pass
