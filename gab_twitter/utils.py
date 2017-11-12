import pandas as pd

def flatten_post_to_dict(post_dict):
   ''' Nested objects are denoted by double underscore (__)
   Flattens a gab post to a dictionary to easily make DataFrame
   There is more room to flatten in attachment and replies objects
   '''
   row = {}
   # meta columns
   row['id'] = post_dict['id']
   row['published_at'] = post_dict['published_at']
   row['type'] = post_dict['type']
   # user columns
   row['actuser__id'] = post_dict['actuser']['id']
   row['actuser__is_donor'] = post_dict['actuser']['is_donor']
   row['actuser__is_investor'] = post_dict['actuser']['is_investor']
   row['actuser__is_private'] = post_dict['actuser']['is_private']
   row['actuser__is_pro'] = post_dict['actuser']['is_pro']
   row['actuser__name'] = post_dict['actuser']['name']
   row['actuser__username'] = post_dict['actuser']['username']
   row['actuser__verified'] = post_dict['actuser']['verified']
   # posts columns (not included:'embed') 
   row['post__attachment_post'] = post_dict['post']['attachment']  # dictionary
   row['post__body'] = post_dict['post']['body']
   row['post__bookmarked'] = post_dict['post']['bookmarked']
   row['post__category'] = post_dict['post']['category']
   row['post__category_details'] = post_dict['post']['category_details']
   row['post__created_at'] = post_dict['post']['created_at']
   row['post__dislike_count'] = post_dict['post']['dislike_count']
   row['post__disliked'] = post_dict['post']['disliked']
   row['post__edited'] = post_dict['post']['edited']
   row['post__id'] = post_dict['post']['id']
   row['post__is_quote'] = post_dict['post']['is_quote']
   row['post__is_replies_disabled'] = post_dict['post']['is_replies_disabled']
   row['post__is_reply'] = post_dict['post']['is_reply']
   row['post__language'] = post_dict['post']['language']
   row['post__like_count'] = post_dict['post']['like_count']
   row['post__liked'] = post_dict['post']['liked']
   row['post__nsfw'] = post_dict['post']['nsfw']
   row['post__only_emoji'] = post_dict['post']['only_emoji']
   row['post__replies_post_dict'] = post_dict['post']['replies']['data']  # <LIST OF POSTS> , can apply recursively?
   row['post__reported'] = post_dict['post']['reported']
   row['post__repost'] = post_dict['post']['repost']
   row['post__revised_at'] = post_dict['post']['revised_at']
   row['post__score'] = post_dict['post']['score']
   return row

def make_dataframe_from_posts(list_of_posts):
   '''input: list of raw post dictionary returned from the API'''
   rows = [flatten_post_to_dict(post) for post in list_of_posts]
   return pd.DataFrame(rows)



