# DuplicateBot
Bot for duplicates


# How to use

* Unzip
* Go into the modules folder and create login.py with the following code:

```python
import praw

reddit = praw.Reddit(username = 'yourusername', password = 'yourpassword', client_id = 'yourclientid', client_secret = 'yourclientsecret', user_agent='DuplicatesBot by /u/PokestarFan')
```




* Use

# Extra scripts

There are extra scripts that come with the bot.

## Delete.py

This script will delete any comment if a person comments delete. It is a mandatory run.

## gb-bb.py

This script controls the good bot/bad bot reply part. It is optional.

## lowpostremover.py

This script removes any comment below 1 karma. It is optional but recommended.

## deleteallcomments.py

If the bot has screwed up and made major mistakes, this script will delete all of the bot's comments.
