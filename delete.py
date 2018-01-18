import logging
import time

from modules.logger import setup_logger
from modules.login import reddit

logger = setup_logger('user_removed_comments')


def main():
    try:
        for item in reddit.inbox.stream():
            logger.debug('On item {}'.format(str(item)))
            try:
                if 'delete' in item.body.lower() and item.author == item.submission.author:
                    item.parent().delete()
                    logging.info('Comment {} removed'.format(str(item.parent())))
                    item.author.message('Removal of comment {}'.format(str(item.parent())),
                                        'The top level post has been removed.')
            except AttributeError:
                pass
            except:
                logging.debug('Item {} skipped'.format(str(item)))
    except(KeyboardInterrupt):
        raise KeyboardInterrupt
    except:
        logging.error('Error!', exc_info=True)
        main()


while True:
    main()
    time.sleep(30)
