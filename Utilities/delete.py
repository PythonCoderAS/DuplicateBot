import praw
from login import reddit


def main(limit, count=0):
	for comment in r.redditor(str(user)).comments.new(limit=limit):
		comment.delete()
		count = count + 1
		print('Finished comment #'+str(count))
		
if __name__ == '__main__':
	limit = input('How many recent comments to delete? Type None for all comments')
	count = 0
	main(limit, count)
	print('Complete')