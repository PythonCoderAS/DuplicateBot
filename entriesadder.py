import logging

from pokestarfansloggingsetup import setup_logger

from modules.entrylogin import reddit

logger = setup_logger('usersubblocker')


def write_to_user_file(text):
    with open('blockusers.txt', 'a') as file:
        file.write(text)


def write_to_sub_file(text):
    with open('blockedsubs.txt', 'a') as file:
        file.write(text)


def strip_message(message):
    try:
        if message.subject == 'remove subreddit':
            subreddit = reddit.subreddit(message)
            mod = False
            for moderator in reddit.subreddit(subreddit).moderator():
                if str(message.author) == str(moderator):
                    mod = True
                    break
            if mod:
                write_to_sub_file(message.body)
            else:
                message.reply('You are not a moderator of the subreddit so your request has not been preformed.')
        elif message.subject == 'remove user':
            if str(message.author) == message.body:
                write_to_user_file(message.body)
            else:
                message.reply('You are not the OP of the submission so your request has not been preformed.')
    except Exception:
        logging.warning('', exc_info=True)


def check_for_messages(reddit):
    try:
        for message in reddit.inbox.unread(mark_read=True):
            strip_message(message)
            reddit.inbox.mark_read(message)
    except Exception:
        logging.error('error!', exc_info=True)


while True:
    check_for_messages(reddit)
