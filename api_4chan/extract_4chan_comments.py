# Python macro using the 4chan API to access 4chan board and extracting infromation from threads and comments into
# a CSV file.

# import libraries
# if basc_4chan library is missing, install with pip3 basc-py4chan
import basc_py4chan

# import more libraries
import pandas as pd

def main():
    # choose output CSV file
    output_csv = "test_4chan.csv"

    # open your favorite board
    boardname = 'pol'
    board = basc_py4chan.Board(boardname)

    # create a dataframe to store infromation from 4chan board
    df = pd.DataFrame( columns = [
            'Thread',
            'Sticky?',
            'Closed?',
            'Topic Post',
            'Postnumber',
            'Timestamp',
            'Datetime',
            'Subject',
            'Comment',
            'File',
            ] )

    # grab all thread ID's 
    thread_ids = board.get_all_thread_ids()
    str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
    print('There are', len(thread_ids), 'active threads on /',boardname,'/:', ', '.join(str_thread_ids))

    # grab a thread (@TODO: Loop over all threads)
    thread = board.get_thread(148985682)

    # thread information
    print('Thread',  thread)
    print('Sticky?', thread.sticky)
    print('Closed?', thread.closed)

    # topic information - loop oever all topics
    all_posts = thread.all_posts
    for post in all_posts:
         print('Topic Post', post)
         print('Postnumber', post.post_number)
         print('Timestamp',  post.timestamp)
         print('Datetime',   repr(post.datetime))
         print('Subject',    post.subject)
         print('Comment',    post.text_comment)
         print('File',    post.file)

         # append to dataframe
         df.loc[len(df)] = [
             thread,
             thread.sticky,
             thread.closed,
             post,
             post.post_number,
             post.timestamp,
             repr(post.datetime),
             post.subject,
             post.text_comment,
             post.file
             ]

    # print head of created dataframe
    print(df.head())

    # write dataframe to CSV output file
    df.to_csv( path_or_buf = output_csv )


# main function to run macro from command line
if __name__ == '__main__':
    main()
