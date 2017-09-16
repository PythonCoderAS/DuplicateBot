import praw
from modules.logger import setup_logger
from modules.login import reddit
import logging

logger = setup_logger('remallcomments')


def main(count=0):
	for comment in r.redditor(str(r.user.me())).comments.new(limit=None):
		comment.delete()
		logging.info('Finished comment #'+str(count)+', id {}'.format(str(comment)))
		
if __name__ == '__main__':
	while True:
		try: 
			main()
		except:
			logging.error('Error!', exc_info=True)