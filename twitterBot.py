#! /usr/bin/python3
# twitterBot.py - Simple twitter bot... work in progress

import tweepy, sys
from myappkeys import myappkeys
 
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

    def tweetSearchReply(self, term):# search and reply to term
        # search 
        results = self.api.search(q=term)
        #reply to users
        for i in results:
            if term == i.text:
                user = i.user.screen_name
                msg = '@%s Hello. My bot has replied to your tweet! :)' % (user)
                # self.tweet(msg)
                self.api.update_status(status=msg, in_reply_to_status_id=i.id)

    def listFollowers(self):    # List all followers 
        for follower in tweepy.Cursor(self.api.followers).items():
            print (follower.screen_name)

 
if __name__ == "__main__":
    twitter = TwitterAPI()
    # twitter.tweet("I'm posting a tweet using my python bot!")
    if len(sys.argv) > 1:
        if sys.argv[1] == 'search':
            term = ' '.join(sys.argv[2:])
            twitter.tweetSearchReply(term)
            # print(term)
        elif sys.argv[1] == 'followers':
            twitter.listFollowers()

