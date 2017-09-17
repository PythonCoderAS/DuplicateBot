import praw
from modules.logger import setup_logger
from modules.login import reddit
import logging
from modules.footer import footer

logger = setup_logger('good_bot_bad_bot')

def main():
	try:
		for item in reddit.inbox.stream():
			written_to = 0
			text = ''
			with open('comments_written_to.txt', 'r') as file:
				for line in file.readlines():
					if line == str(item) and written_to == 0:
						written_to = 1
						logging.info('Comment {} has been already replied to.'.format(str(item)))
			if written_to == 0:
				if 'good bot' in str(item.body.lower()):
					text = 'Good human'
					item.reply(text+footer)
					logging.info('Message with the text {} replied to comment {}'.format(text, str(item)))
					with open('comments_written_to.txt', 'a') as file:
						file.write(str(item)+'\n')
				elif 'bad bot' in str(item.body.lower()):
					text = 'Bad human'
					item.reply(text+footer)
					logging.info('Message with the text {} replied to comment {}'.format(text, str(item)))
					with open('comments_written_to.txt', 'a') as file:
						file.write(str(item)+'\n')
				elif 'average bot' in str(item.body.lower()):
					text = 'Average human'
					item.reply(text+footer)
					logging.info('Message with the text {} replied to comment {}'.format(text, str(item)))
					with open('comments_written_to.txt', 'a') as file:
						file.write(str(item)+'\n')
				elif 'bot' in str(item.body.lower()):
					strings = str(item.body.lower()).split('bot')
					text = '{} human'.format(strings[0])
					item.reply(text+footer)
					logging.info('Message with the text {} replied to comment {}'.format(text, str(item)))
					with open('comments_written_to.txt', 'a') as file:
						file.write(str(item)+'\n')
	except(KeyboardInterrupt):
		raise KeyboardInterrupt
	except:
		logging.error('Error', exc_info = True)
		
if __name__ == '__main__':
	while True:
		try:
			main()
		except(KeyboardInterrupt):
			raise KeyboardInterrupt