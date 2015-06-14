#! /usr/bin/python3
# twitterBot.py - Simple twitter bot... work in progress

import tweepy, sys
from myappkeys import myappkeys

idFile = 'list_of_twitter_ids_bot_replied.txt'
IGNORE_LIST = []
 
class TwitterAPI:
    def __init__(self):
        consumer_key = myappkeys['consumer_key']
        consumer_secret = myappkeys['consumer_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = myappkeys['access_token']
        access_token_secret = myappkeys['access_token_secret']
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
 
    def tweet(self, message):
        # Post 
        self.api.update_status(status=message)

    def tweetSearchReply(self, term):
        """ search and reply to term """
        # search 
        results = self.api.search(q=term)
        #reply to users
        for i in results:
            if term == i.text and  not(check_id(i.id)):
                user = i.user.screen_name
                msg = '@%s Hello. My bot has replied to your tweet! :)' % (user)
                # self.tweet(msg)
                self.api.update_status(status=msg, in_reply_to_status_id=i.id)
                IGNORE_LIST.append(i.id)  
        # write_ids_to_File()
        # print(IGNORE_LIST)
    

    def listFollowers(self):    
        """ List all followers """
        for follower in tweepy.Cursor(self.api.followers).items():
            print (follower.screen_name)


def write_ids_to_File():
        """ write IGNORE_LIST to file """
        try:
            f = open(idFile, 'w')
            for i in IGNORE_LIST:
                f.write(i + '\n')
            f.close()
        except IOError:
            raise 'Error writing file!'
    
def get_last_id(id):
    """ returns list of ids bot replied"""
    try:
        with open(idFile) as f:
            IGNORE_LIST = f.read().splitlines()
        f.close()
    except IOError:
        return ''

def check_id(id):
    """ Checks IGNORE_LIST for id """
    for i in IGNORE_LIST:
        if id == i:
            return True 
    return False

def main():
    usage = '\nUsage:\t twitterBot.py <keyword> { search term }\n\t <> is required\n\t {} is conditional\n'
    
    twitter = TwitterAPI()
    

    if len(sys.argv) > 1:
        if sys.argv[1] != 'search' and sys.argv != 'followers':
            print(usage)
        elif sys.argv[1] == 'search':
            term = ' '.join(sys.argv[2:])
            twitter.tweetSearchReply(term)
            # print(term)
        elif sys.argv[1] == 'followers':
            twitter.listFollowers()
    else:
        print(usage)

if __name__ == "__main__":
    main()