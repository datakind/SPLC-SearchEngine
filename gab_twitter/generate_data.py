''' generate_data.py

Outline to build data sets for analysis.
Lots of work to do here still, no testing has been done yet
'''

import pandas as pd

from gab_api import *
from twitter_api import *

TARGET_USER = ''
MASTER_OUTPUT_DIRECTORY = ''
OUTPUT_DIRECTORY = MASTER_OUTPUT_DIRECTORY + 'posts/'


tw = twitter_connect(TWITTER_API_KEYS)
gab_session = start_session(login_payload)


def is_gab_acct(twitter_user):
	pass

def find_gab_acct(twitter_user):
	pass

class UserOfInterest(object):
	"""docstring for UserOfInterest"""
	def __init__(self, gab_username, twitter_screen_name, gab_posts, tweets):
		self.gab_username = gab_username
		self.twitter_screen_name = twitter_screen_name
		self.gab_posts = gab_posts
		self.tweets = tweets
		self.id = '{}_{}'.format(gab_username, twitter_screen_name)
		
def get_user_data():
	target_twitter_followers = get_followers(
		tw,
		TARGET_USER, 
		user_fields=['description', 'lang', 'name']
		)

	overlapping_followers = filter(is_gab_acct, target_twitter_followers)
	users_of_interest = []
	# need to add some serious exception handling and retrying
	# needs to account for the datatype in overlapping followers
	for user in overlapping_followers:
		tw_sceen_name = user #.screen_name
		gab_username = find_gab_acct(user)
		gab_posts = get_user_feed(gab_username, gab_session, write_path=OUTPUT_DIRECTORY)
		tweets = get_tweets(user)
		users_of_interest.append(
			UserOfInterest(gab_username, tw_sceen_name, gab_posts, tweets)
			)
	return users_of_interest

if __name__ == '__main__':
	user_data = get_user_data()
	# aggregate data
	tweets_df = pd.concat([user.tweets for user in user_data])
	posts_df = pd.concat([user.gab_posts for user in user_data])
	# write data
	tweets_df.to_csv('tweets.csv', index=False)
	posts_df.to_csv('gab_posts.csv', index=False)
