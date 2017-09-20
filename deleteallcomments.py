import praw
from modules.logger import setup_logger
from modules.login import reddit as r
import logging

logger = setup_logger('remove_all_comments')


def main(count=0):
	for comment in r.redditor(str(r.user.me())).comments.new(limit=None):
		comment.delete()
		logging.info('Finished comment #'+str(count)+', id {}'.format(str(comment)))
		count += 1
		
if __name__ == '__main__':
	while True:
		try: 
			main()
		except:
			logging.error('Error!', exc_info=True)