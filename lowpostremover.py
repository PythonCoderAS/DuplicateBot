#Bot to remove any submissions by the user that have negative scores
#Created for /u/Pokestarfan
#Created by reddit /u/dustonwithano
#Please PM me on reddit with any issues

###########################
# import modules                      
###########################

import time
import praw
from login import reddit as r

###########################
# definitions                     
###########################

#defining the log in process
global r

#definig the value: CREATED BY POKESTARFAN AFTER RECIVIAL
setvalue = 1

#defining the searching and removal
def action():
    global submission_titles #making global submission title list
    global comment_submissions #making glocal comment submission title list
    comment_submissions = []
    submission_titles = []
    submission_number = 0
    comment_number = 0
    current_submission_number = 0
    current_comment_number = 0
    print('Searching...')
    user = r.user.me()
    for submission in r.redditor(str(user)).submissions.new(limit=None): #scanning all submissions by reddit user without limit
        if submission.score < setvalue: #if statement checking the submission score < 0
           submission.delete() #deleting the submission
           submission_titles.append(submission.title) #adding the submission title to the list
    for comment in r.redditor(str(user)).comments.new(limit=None): #scanning all comments by reddit user without limit
        if comment.score < setvalue: #if statement checking the comment score < 0 
           comment.delete() #deleteing the comment if < 0
           comment_submissions.append(comment.submission.title) #adding the comment's original submission title to the list
           
#defining the outputs
def print_results():
    print('Search Complete')
    print('--------------------------------------------------')
    #if statement. True if there is 1 or more submissions removed. 
    if len(submission_titles) > 0:
        #printing true results
        print('Removed ' + str(len(submission_titles)) + ' submission(s).')
        print('Submission title(s) include: ')
        print(*submission_titles, sep='\n') #printing submission titles with line breaks
        print('--------------------------------------------------')
    else:
        #printing false results
        print('No submissions removed.')
        print('--------------------------------------------------')
    #if statement. True if there is 1 or more comments removed. 
    if len(comment_submissions) > 0:
        #printing true results
        print('Removed ' + str(len(comment_submissions)) + ' comment(s).')
        print('Comments were under the following submissions: ')
        print(*comment_submissions, sep='\n') #printing comment's submission's titles with line breaks
        print('--------------------------------------------------')
    else:
        #printing false results
        print('No comments removed.')
        print('--------------------------------------------------')

###########################
# code execution
###########################


def main():
    action()
    print_results()
	
while True:
    main()
    time.sleep(600)