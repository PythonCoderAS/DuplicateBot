#Bot to remove any submissions by the user that have negative scores
#Created for /u/Pokestarfan
#Created by reddit /u/dustonwithano
#Please PM me on reddit with any issues

###########################
# import modules                      
###########################

import time
import praw
from modules.logger import setup_logger
from modules.login import reddit as r
import logging

logger = setup_logger('low_score_remover')

###########################
# definitions                     
###########################

#defining the log in process
global r

#definig the value: CREATED BY POKESTARFAN AFTER RECIVIAL
setvalue = 1

#defining the searching and removal
def action():
    global comment_submissions #making glocal comment submission title list
    comment_submissions = []
    submission_titles = []
    submission_number = 0
    comment_number = 0
    current_submission_number = 0
    current_comment_number = 0
    logging.info('Searching...')
    user = r.user.me()
    for comment in r.redditor(str(user)).comments.new(limit=None): #scanning all comments by reddit user without limit
        logging.debug('On comment {}'.format(str(comment)))
        if comment.score < setvalue: #if statement checking the comment score < 0 
           comment.delete() #deleteing the comment if < 0
           logging.info('Removed comment {}'.format(str(comment)))
           comment_submissions.append(comment.submission.title) #adding the comment's original submission title to the list
           
#defining the outputs
def print_results():
    logging.info('Search Complete')
    logging.info('--------------------------------------------------')
    #if statement. True if there is 1 or more comments removed. 
    if len(comment_submissions) > 0:
        #logging.infoing true results
        logging.info('Removed ' + str(len(comment_submissions)) + ' comment(s).')
        logging.info('Comments were under the following submissions: ')
        logging.info(*comment_submissions, sep='\n') #logging.infoing comment's submission's titles with line breaks
        logging.info('--------------------------------------------------')
    else:
        #logging.infoing false results
        logging.info('No comments removed.')
        logging.info('--------------------------------------------------')

###########################
# code execution
###########################


def main():
    action()
    print_results()
    
while True:
    main()