import praw
from modules.logger import setup_logger
from modules.login import reddit
from modules.footer import footer
import logging
import time

logger = setup_logger('user_removed_comments')


def main():
	try:
		for item in reddit.inbox.stream():
			logger.debug('On item {}'.format(str(item)))
			try:
				if 'delete' in item.body.lower():
					item.parent().delete()
					logging.info('Comment {} removed'.format(str(item.parent())))
					item.reply('The top level post has been removed.'+footer)
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