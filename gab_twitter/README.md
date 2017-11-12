# Goal
The goal of this project was to identify 'influential' users on gab.ai and build a dataset of their information they are sharing on gab or twitter.

The idea is that you can find an overal of users between both platforms where gab shows a more raw and uncleaned version of the information these users are sharing or consuming while twitter is one step closer to mainstream information. These identified users can be seen as propagators of a certain kind of information and can set the stage for what people are exposed to in each platform. Understanding what they see and what they share can help understand what topics people are talking about in these circles.

With this data, we can apply topic modeling analyses and we can featurize all of their posts for further exploration (ex: the gab posts were flattened to ~36 columns).

# Contents
* gab_api.py - this contains group of functions that work on a very bare API from gab.ai. The main function here builds a pandas dataframe for a given user's latest posts. See utils.py for the available columns. There is also a function to search arbitrary keywords which returns raw responses for now.
* twitter_api.py - this is a working version of a way to get lists of followers for a given twitter screen name. Twitter has a bunch of rate limits on the api which have complicated this step.
* credentials.py - this contains dictionaries with necessary credentials for each file. Should be updated as needed.
* utils.py - helper functions to build gab post data frames
* andrewwanglin_posts.csv - sample output of @andrewwaglin's latest posts on gab.ai
* examples.ipynb - python notebook with simple examples
* generate_data.py - work in progress script to pull it all together and generate posts/feeds for users of interest

# Potential Next Steps
The main methodology would be as follows:
* finish generate_data.py
** identify users of high interest
** find overlap of users on twitter and gab.ai and pull posts/tweets for analysis and modeling
* It would also be useful to build a more robust object-oriented wrapper for these APIs, along with more exception handing and retrying.
* set up something to automatically track and store the gab posts of these high interest users

# More details
(more outlined in generate_data.py)
Get a list of twitter users and see if they have a gab.ai presence:
* check their bios to search for gab profiles
* is there someone one on gab with a similar name/username/etc on twitter?

Need a way to determine list of users to check for on gab:
* followers of Trump/Coulter/Breitbart/Gab/etc...
* users under a specific search/topic/hashtag
* because of Twitter API rate limits this list should be generated over time and stored externally

Once we have overlapping users of interest, we can aggregate the gab posts and the tweets to build a dataset. Since gab only allows the most recent ~28 posts in the responses, it would be beneficial to write the posts to a database on a recurring basis.