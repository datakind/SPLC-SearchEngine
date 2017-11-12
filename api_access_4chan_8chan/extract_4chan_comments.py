# Python macro using the 4chan API to access 4chan board and extracting infromation from threads and comments into
# a CSV file.

# check that these libraries are installed- install (using pip) if not:
# - pandas
# - basc-py4chan
# - progressbar2

# import libraries
import sys
import pandas as pd

import basc_py4chan
from progressbar import ProgressBar

# clean up function
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def main():

    # chech command line input parameters
    if len(sys.argv) != 3:
        print("Usage: python %s [board] [output.csv]" % sys.argv[0])
        print("Extracts all comments on board into csv file.")
        print("Example: python %s pol comments_4chan_pol.csv"
              % sys.argv[0])
        #sys.exit(1)
        return

    # open your favorite board
    boardname = sys.argv[1]
    board = basc_py4chan.Board(boardname)

    # choose output CSV file
    output_csv = sys.argv[2]

    # create a dataframe to store infromation from 4chan board
    df = pd.DataFrame( columns = [
            'Thread',
            'Sticky?',
            'Closed?',
            'Posts_in_thread',
            'Topic Post',
            'Postnumber',
            'Timestamp',
            'Datetime',
            'Name',
            'Subject',
            'Comment',
            'File'
            ] )

    # grab all thread ID's 
    thread_ids = board.get_all_thread_ids()
    str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
    print('There are', len(thread_ids), 'active threads on /',boardname,'/:', ', '.join(str_thread_ids))

    # prepare progress bar
    print( 'Progress:' )
    pbar = ProgressBar()

    # loop over all threads
    for thread_id in pbar( thread_ids ) :
        thread = board.get_thread( thread_id )

        # topic information - loop oever all topics
        all_posts = thread.all_posts

        # skip if all_posts not found
        if ( all_posts == None ):
            continue

        # if all_posts found, extract all comments
        for post in all_posts:

            # clean up text in tsubject field
            if ( post.subject ):
                subject_clean = clean(post.subject)
            else:
                subject_clean = 'N/A'

            # clean up text in text_comment field
            comment_clean = clean(post.text_comment)

            # append to dataframe
            df.loc[len(df)] = [
                thread,
                thread.sticky,
                thread.closed,
                len(all_posts),
                post,
                post.post_number,
                post.timestamp,
                repr(post.datetime),
                post.name,
                subject_clean,
                comment_clean,
                post.file
                ]

    # print head of created dataframe
    #print(df.head())

    # write dataframe to CSV output file
    df.to_csv( path_or_buf = output_csv )


# main function to run macro from command line
if __name__ == '__main__':
    main()
