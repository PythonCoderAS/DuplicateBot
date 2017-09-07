import re
import praw
from login import reddit

def action():
    for sub_id in reddit.subreddit('all').stream.submissions():
        blockeduser = 0
        item_written_to = 0
        for item in reddit.inbox.unread(limit=None):
            if str(item.subject) == 'Remove me from posts':
                body = str(item.body)
                yes = re.search('\/u\/[a-zA-Z0-9]+',body)
                username = yes.group(0)
                if str(item.author) == username:
                    with open('blockedusers.txt', 'a') as file:
                        newstring = username.replace(r'/u/','')
                        file.write(newstring)
        with open('posts_written_to.txt','r') as writefile:
            for id_to_use in writefile.readlines():
                if item_written_to == 0:
                    if sub_id == id_to_use:
                        item_written_to = 1
        duplicates = []
        submission = praw.models.Submission(reddit, id = sub_id)
        with open('blockusers.txt','r') as newfile:
            for line in newfile.readlines():
                if submission.author == line and blockeduser == 0:
                    pass
                else:
                    blockeduser = 1
        if blockeduser == 0 and item_written_to == 0:
            for duplicate in submission.duplicates():            
                dup_sub = praw.models.Submission(reddit, id = duplicate)
                duplicates.append({'title':str(dup_sub.title), 'subreddit':str(dup_sub.subreddit), 'link':str(
                    dup_sub.shortlink)})
                if len(duplicates) > 0:
                    message = 'Here is a list of threads in other subreddits about the same content:\n'
                    for dup in duplicates:
                        message = str(message + '\n # [{}]({}) on /r/{}').format(dup['title'], dup['link'], dup['subreddit'])
                    message = message + '\n\n ---- \n\n ^^I^^am^^a^^bot^^[FAQ](https://www.reddit.com/r/DuplicatesBot/wiki/index)-[Code](https://github.com/PokestarFan/DuplicateBot-[Bugs](https://www.reddit.com/r/DuplicatesBot/comments/6ypgmx/bugs_and_problems/)-[Suggestions](https://www.reddit.com/r/DuplicatesBot/comments/6ypg85/suggestion_for_duplicatesbot/)-[How to block](https://www.reddit.com/r/DuplicatesBot/wiki/index#wiki_block_bot_from_tagging_on_your_posts'
            try:
                submission.reply(message)
                with open('writes.log', 'a') as logfile:
                        logfile.write('Replied to submission id {}'.format(sub_id))
                        print('Replied to submission id {}'.format(sub_id))
                        with open('posts_written_to.txt','a') as writefile2:
                            writefile2.write(sub_id)
            except(UnboundLocalError):
                pass
        

if __name__ == '__main__':
    action()