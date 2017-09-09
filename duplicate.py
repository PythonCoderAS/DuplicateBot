import datetime
import logging
import praw
import prawcore
import sys
from login import reddit


file_handler = logging.FileHandler(filename='duplicates.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)

def action():
    for sub_id in reddit.subreddit('all').stream.submissions():
        logging.debug('Starting submission {}'.format(sub_id))
        blockeduser = 0
        duplicates = []
        submission = praw.models.Submission(reddit, id = sub_id)
        with open('blockusers.txt','r') as newfile:
            for line in newfile.readlines():
                line = line.strip('\n')
                if str(submission.author) == line:
                    blockeduser = 1
                    logger.debug('User {}\'s submission {} was blocked from posting'.format(str(submission.author),str(sub_id)))
                else:
                    pass
        if blockeduser == 0:
            for duplicate in submission.duplicates():            
                dup_sub = praw.models.Submission(reddit, id = duplicate)
                if 'ImagesOf' not in str(dup_sub.subreddit) and 'auto' not in str(dup_sub.subreddit):
                    time = dup_sub.created
                    time = str(datetime.datetime.fromtimestamp(time))
                    author = str(dup_sub.author)
                    if str(submission.author) == author:
                        author = author + '[author of both threads]'
                    duplicates.append({'title':str(dup_sub.title), 'subreddit':str(dup_sub.subreddit), 'link':'https://www.reddit.com'+str(dup_sub.permalink), 'time':str(time), 'author':author})
                    if len(duplicates) > 0:
                        message = 'Here is a list of threads in other subreddits about the same content:\n'
                        for dup in duplicates:
                            message = str(message + '\n * [{}]({}) on /r/{} (created at {} by {})').format(dup['title'], dup['link'], dup['subreddit'], dup['time'], dup['author'])
                        message = message + '\n\n ---- \n\n ^^I ^^am ^^a ^^bot  ^^[FAQ](https://www.reddit.com/r/DuplicatesBot/wiki/index)-[Code](https://github.com/PokestarFan/DuplicateBot-[Bugs](https://www.reddit.com/r/DuplicatesBot/comments/6ypgmx/bugs_and_problems/)-[Suggestions](https://www.reddit.com/r/DuplicatesBot/comments/6ypg85/suggestion_for_duplicatesbot/)-[Block](https://www.reddit.com/r/DuplicatesBot/wiki/index#wiki_block_bot_from_tagging_on_your_posts)'
            try:
                submission.reply(message)
                logger.info('Message posted on {}'.format(sub_id))
                message = ''
            except(praw.exceptions.APIException, UnboundLocalError):
                logger.info('Submission {} has been skipped due to missing text'.format(sub_id))
                message = ''
            except(prawcore.exceptions.Forbidden):
                logger.info('You are blocked on /r/{}'.format(str(submission.subreddit)))
                message = ''
            except:
                logger.error('Error occured!', exc_info=True)
                message = ''
            

if __name__ == '__main__':
    while True:
        try:
            action()
        except(KeyboardInterrupt):
            raise KeyboardInterrupt
        except:
            logger.critical('Error has occured when running main loop, please resolve asap', exc_info=True)