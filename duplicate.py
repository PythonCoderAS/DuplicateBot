import logging
from datetime import datetime

import praw
import prawcore
from pokestarfansloggingsetup import setup_logger

from modules.login import reddit
from modules.table import starter

logger = setup_logger('duplicates')


# noinspection PyBroadException
def generate_and_reply(submission):
    footer = '\n\n----\n\n ^^I ^^am ^^a ^^bot  ^^[FAQ](https://www.reddit.com/r/DuplicatesBot/wiki/index)-[' \
                      'Code](https://github.com/PokestarFan/DuplicateBot)-[Bugs](' \
                      'https://www.reddit.com/r/DuplicatesBot/comments/6ypgmx/bugs_and_problems/)-[Suggestions](' \
                      'https://www.reddit.com/r/DuplicatesBot/comments/6ypg85/suggestion_for_duplicatesbot/)-[Block ' \
                      'user (op only)' \
                      '](' \
                      'https://www.reddit.com/message/compose/?to=DuplicatesBotBlocker&subject=remove%20user&message' \
                      '={user})-[Block from subreddit (mods only)](' \
                      'https://www.reddit.com/message/compose/?to=DuplicatesBotBlocker&subject=remove%20subreddit' \
                      '&message={sub})\n' \
                      '\n^^Now ^^you ^^can ^^remove ^^the ^^comment ^^by ^^replying ^^delete! '.format(user=
    str(
        submission.author), sub=str(submission.subreddit))
    global message
    sub_id = submission.subreddit
    for dup_sub in submission.duplicates():
        duplicates = []
        time = dup_sub.created
        time = str(datetime.fromtimestamp(time))
        author = '/u/' + str(dup_sub.author)
        if str(submission.author) == author:
            author = author + ' [author of both threads]'
        duplicates.append(['[{}]({})'.format(str(dup_sub.title), 'https://www.reddit.com' + str(dup_sub.permalink)),
                           str(dup_sub.subreddit), author, str(time), str(dup_sub.score)])
        if len(duplicates) > 0:
            message = 'Here is a list of threads in other subreddits about the same content:\n'
            for dup in duplicates:
                starter.add_row_with_list(dup)
                message += '\n' + starter.table
            message += '\n' + footer
    try:
        submission.reply(message)
        logger.info('Message posted on {}'.format(sub_id))
        logger.debug('Message: {}'.format(message))
        message = ''
    except praw.exceptions.APIException:
        logger.debug('Submission {} has been skipped due to missing text.'.format(sub_id))
        message = ''
    except prawcore.exceptions.Forbidden:
        logger.debug('You are blocked on /r/{}'.format(str(submission.subreddit)))
        message = ''
    except AssertionError:
        logger.debug('Assertion Error occured! Printing message and traceback.')
        logger.debug(message + str(len(message)), exc_info=True)
        message = ''
    except(KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        logger.error('Error occurred!', exc_info=True)
        message = ''
    except:
        logger.critical(
            'Massive Error occurred! Not part of the Exception, KeyboardInterrupt or SystemExit exceptions. Fix ASAP.',
            exc_info=True)
        message = ''


def run_bot(sub_id):
    global blocked_sub
    if True:
        try:
            logging.debug('Starting submission {}'.format(str(sub_id)))
            blocked_user = 0
            blocked_sub = 0
            submission = sub_id
            try:
                with open('blockusers.txt', 'r') as new_file:
                    for line in new_file.readlines():
                        line = line.strip('\n')
                        if str(submission.author).lower() == line.lower() or 'bot' in str(submission.author).lower():
                            blocked_user = 1
                            break
            except FileNotFoundError:
                with open('blockusers.txt', 'w'):
                    blocked_user = 0
            try:
                with open('blockedsubs.txt', 'r') as new_file:
                    for line in new_file.readlines():
                        line = line.strip('\n')
                        if str(submission.subreddit).lower() == line.lower():
                            blocked_sub = 1
                            break
            except FileNotFoundError:
                with open('blockedsubs.txt', 'w'):
                    blocked_sub = 0
            if blocked_user == 0 and blocked_sub == 0:
                generate_and_reply(sub_id)
        except(KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            logger.error('Error on submission {} occurred.'.format(str(sub_id)), exc_info=True)


def action():
    for sub_id in reddit.subreddit('all').stream.submissions():
        run_bot(sub_id)


if __name__ == '__main__':
    while True:
        try:
            action()
        except(KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            logger.critical('Error has occured when running main loop, please resolve asap', exc_info=True)
