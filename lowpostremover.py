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
# defistarnitions                     
###########################

#defining the log in process
global r

#definig the value: CREATED BY POKESTARFAN AFTER RECIVIAL
setvalue = 1

#defining the searching and removal
def action():
    logging.info('Searching...')
    user = r.user.me()
    for comment in r.redditor(str(user)).comments.new(limit=None): #scanning all comments by reddit user without limit
        logging.debug('On comment {}'.format(str(comment)))
        if comment.score < setvalue: #if statement checking the comment score < 0 
           comment.delete() #deleteing the comment if < 0
           logging.info('Removed comment {}'.format(str(comment)))

while True:		   
	action()
	time.sleep(60)