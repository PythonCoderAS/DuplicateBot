#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
#  PPPPPPPPPPPPPPPPP                   kkkkkkkk                                                      tttt                                             FFFFFFFFFFFFFFFFFFFFFF                                 
#  P::::::::::::::::P                  k::::::k                                                   ttt:::t                                             F::::::::::::::::::::F                                 
#  P::::::PPPPPP:::::P                 k::::::k                                                   t:::::t                                             F::::::::::::::::::::F                                 
#  PP:::::P     P:::::P                k::::::k                                                   t:::::t                                             FF::::::FFFFFFFFF::::F                                 
#    P::::P     P:::::P  ooooooooooo    k:::::k    kkkkkkk eeeeeeeeeeee        ssssssssss   ttttttt:::::ttttttt      aaaaaaaaaaaaa  rrrrr   rrrrrrrrr   F:::::F       FFFFFFaaaaaaaaaaaaa  nnnn  nnnnnnnn    
#    P::::P     P:::::Poo:::::::::::oo  k:::::k   k:::::kee::::::::::::ee    ss::::::::::s  t:::::::::::::::::t      a::::::::::::a r::::rrr:::::::::r  F:::::F             a::::::::::::a n:::nn::::::::nn  
#    P::::PPPPPP:::::Po:::::::::::::::o k:::::k  k:::::ke::::::eeeee:::::eess:::::::::::::s t:::::::::::::::::t      aaaaaaaaa:::::ar:::::::::::::::::r F::::::FFFFFFFFFF   aaaaaaaaa:::::an::::::::::::::nn 
#    P:::::::::::::PP o:::::ooooo:::::o k:::::k k:::::ke::::::e     e:::::es::::::ssss:::::stttttt:::::::tttttt               a::::arr::::::rrrrr::::::rF:::::::::::::::F            a::::ann:::::::::::::::n
#    P::::PPPPPPPPP   o::::o     o::::o k::::::k:::::k e:::::::eeeee::::::e s:::::s  ssssss       t:::::t              aaaaaaa:::::a r:::::r     r:::::rF:::::::::::::::F     aaaaaaa:::::a  n:::::nnnn:::::n
#    P::::P           o::::o     o::::o k:::::::::::k  e:::::::::::::::::e    s::::::s            t:::::t            aa::::::::::::a r:::::r     rrrrrrrF::::::FFFFFFFFFF   aa::::::::::::a  n::::n    n::::n
#    P::::P           o::::o     o::::o k:::::::::::k  e::::::eeeeeeeeeee        s::::::s         t:::::t           a::::aaaa::::::a r:::::r            F:::::F            a::::aaaa::::::a  n::::n    n::::n
#    P::::P           o::::o     o::::o k::::::k:::::k e:::::::e           ssssss   s:::::s       t:::::t    tttttta::::a    a:::::a r:::::r            F:::::F           a::::a    a:::::a  n::::n    n::::n
#  PP::::::PP         o:::::ooooo:::::ok::::::k k:::::ke::::::::e          s:::::ssss::::::s      t::::::tttt:::::ta::::a    a:::::a r:::::r          FF:::::::FF         a::::a    a:::::a  n::::n    n::::n
#  P::::::::P         o:::::::::::::::ok::::::k  k:::::ke::::::::eeeeeeee  s::::::::::::::s       tt::::::::::::::ta:::::aaaa::::::a r:::::r          F::::::::FF         a:::::aaaa::::::a  n::::n    n::::n
#  P::::::::P          oo:::::::::::oo k::::::k   k:::::kee:::::::::::::e   s:::::::::::ss          tt:::::::::::tt a::::::::::aa:::ar:::::r          F::::::::FF          a::::::::::aa:::a n::::n    n::::n
#  PPPPPPPPPP            ooooooooooo   kkkkkkkk    kkkkkkk eeeeeeeeeeeeee    sssssssssss              ttttttttttt    aaaaaaaaaa  aaaarrrrrrr          FFFFFFFFFFF           aaaaaaaaaa  aaaa nnnnnn    nnnnnn
#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
#                                                                                                                                                                                                            
import logging
from datetime import datetime

import praw
import prawcore
from markdowntable import Table as ta
from pokestarfansloggingsetup import setup_logger

from modules.login import reddit

logger = setup_logger('duplicates')


# noinspection PyBroadException
def generate_and_reply(submission):
    starter = ta('Title')
    starter.all_columns('Subreddit', 'Author', 'Time', 'Karma')
    footer = '\n\n----\n\n I am a bot [FAQ](https://www.reddit.com/r/DuplicatesBot/wiki/index)-[' \
             'Code](https://github.com/PokestarFan/DuplicateBot)-[Bugs](' \
                      'https://www.reddit.com/r/DuplicatesBot/comments/6ypgmx/bugs_and_problems/)-[Suggestions](' \
                      'https://www.reddit.com/r/DuplicatesBot/comments/6ypg85/suggestion_for_duplicatesbot/)-[Block ' \
                      'user (op only)' \
                      '](' \
                      'https://www.reddit.com/message/compose/?to=DuplicatesBotBlocker&subject=remove%20user&message' \
                      '={user})-[Block from subreddit (mods only)](' \
                      'https://www.reddit.com/message/compose/?to=DuplicatesBotBlocker&subject=remove%20subreddit' \
                      '&message={sub})\n' \
             '\nNow you can remove the comment by replying delete! '.format(user=
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
                           '/r/' + str(dup_sub.subreddit), author, str(time), str(dup_sub.score)])
        if len(duplicates) > 0:
            message = 'Here is a list of threads in other subreddits about the same content:\n'
            for dup in duplicates:
                starter.add_row_with_list(dup)
                message += '\n' + starter.table
            message += '\n' + footer
    try:
        submission.reply(message)
        logger.info('Message posted on {}'.format(str(submission)))
        logger.debug('Message: {}'.format(message))
    except(praw.exceptions.APIException, UnboundLocalError):
        logger.debug('Submission {} has been skipped due to missing text.'.format(sub_id))
    except prawcore.exceptions.Forbidden:
        logger.debug('You are blocked on /r/{}'.format(str(submission.subreddit)))
    except AssertionError:
        logger.debug('Assertion Error occured! Printing message and traceback.')
        logger.debug(message + str(len(message)), exc_info=True)
    except(KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        logger.error('Error occurred!', exc_info=True)
    except:
        logger.critical(
            'Massive Error occurred! Not part of the Exception, KeyboardInterrupt or SystemExit exceptions. Fix ASAP.',
            exc_info=True)
    finally:
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
