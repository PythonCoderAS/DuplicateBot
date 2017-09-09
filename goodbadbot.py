import time
import praw
from login import reddit


def main():
	while True:
		for item in reddit.inbox.all(limit=5):
			with open('replies.txt', 'r') as readfile:
				for line in readfile.readlines():
					if line == item:
						pass
					else:
						try:
							if 'good' and 'bot' in item.body:
								item.reply('Good human')
								with open('replies.txt', 'a') as file:
										file.write(str(item)+'\n')
							elif 'bad' and 'bot' in item.body:
								item.reply('bad human')
								with open('replies.txt', 'a') as file:
									file.write(str(item)+'\n')
						except:
							pass

if __name__ == '__main__':
	main()