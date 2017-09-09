import datetime
import praw
from login import reddit

def action():
    for sub_id in reddit.subreddit('all').stream.submissions():
        blockeduser = 0
        for item in reddit.inbox.messages(limit=5):
            if str(item.subject) == 'Remove me from posts':
                body = str(item.body)
                with open('blockusers.txt', 'a+') as file:
                    if str(item.author) == body and body not in file.read():
                        newstring = username.replace(r'/u/','')
                        newstring = newstring = '\n'
                        file.write(newstring)
        duplicates = []
        submission = praw.models.Submission(reddit, id = sub_id)
        with open('blockusers.txt','r') as newfile:
            for line in newfile.readlines():
                line = line.strip('\n')
                if str(submission.author) == line:
                    blockeduser = 1
                else:
                    pass
        if blockeduser == 0:
            for duplicate in submission.duplicates():            
                dup_sub = praw.models.Submission(reddit, id = duplicate)
                if 'ImagesOf' not in str(dup_sub.subreddit) and 'auto' not in str(dup_sub.subreddit):
                    time = dup_sub.created
                    time = str(datetime.datetime.fromtimestamp(time))
                    author = str(dup_sub.author)
                    if str(submission.author) == author:
                        author = author + '[author of both threads]'
                    duplicates.append({'title':str(dup_sub.title), 'subreddit':str(dup_sub.subreddit), 'link':'https://www.reddit.com'+str(dup_sub.permalink), 'time':str(time), 'author':author})
                    if len(duplicates) > 0:
                        message = 'Here is a list of threads in other subreddits about the same content:\n'
                        for dup in duplicates:
                            message = str(message + '\n * [{}]({}) on /r/{} (created at {} by {})').format(dup['title'], dup['link'], dup['subreddit'], dup['time'], dup['author'])
                        message = message + '\n\n ---- \n\n ^^I ^^am ^^a ^^bot  ^^[FAQ](https://www.reddit.com/r/DuplicatesBot/wiki/index)-[Code](https://github.com/PokestarFan/DuplicateBot-[Bugs](https://www.reddit.com/r/DuplicatesBot/comments/6ypgmx/bugs_and_problems/)-[Suggestions](https://www.reddit.com/r/DuplicatesBot/comments/6ypg85/suggestion_for_duplicatesbot/)-[Block](https://www.reddit.com/r/DuplicatesBot/wiki/index#wiki_block_bot_from_tagging_on_your_posts)'
            try:
                submission.reply(message)
                message = ''
            except:
                pass
                message = ''
            

if __name__ == '__main__':
    while True:
        try:
            action()
        except(KeyboardInterrupt):
            raise KeyboardInterrupt
        except:
            pass