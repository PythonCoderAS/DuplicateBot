import praw
from modules.logger import setup_logger
from modules.login import reddit
import logging

logger = setup_logger('user_removed_comments')

for item in reddit.inbox.stream():
	logger.debug('On item {}'.format(str(item)))
	try:
		if item.body.lower() == 'delete':
			item.parent.delete()
			logging.info('Comment {} removed'.format(str(item.parent)))
			item.reply('The top level post has been removed.')
	except:
		logging.debug('Item {} skipped'.format(str(item)))
		pass