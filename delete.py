import praw
from modules.logger import setup_logger
from modules.login import reddit
import logging
import time

logger = setup_logger('user_removed_comments')


def main():
	try:
		for item in reddit.inbox.comment_replies(limit=30):
			logger.debug('On item {}'.format(str(item)))
			print(item.body)
			try:
				if 'delete' in item.body.lower():
					item.parent.delete()
					logging.info('Comment {} removed'.format(str(item.parent)))
					item.reply('The top level post has been removed.')
			except:
				logging.debug('Item {} skipped'.format(str(item)))
	except:
		logging.debug('Error!', exc_info=True)
		main()
		
while True:
	main()
	time.sleep(30)