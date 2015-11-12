from celery.task import periodic_task, task
from django.conf import settings
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from coreapp.models import Tweet
#Variables that contains the user credentials to access Twitter API 


consumer_key = settings.CK
consumer_secret = settings.CS
access_token = settings.AT
access_token_secret = settings.ATS

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def check_1000(self):
        if Tweet.objects.all().count() < 1000:
            print "ADDED=================>>"
            return True
        print "FULL=================>>>"
        return False
    def on_data(self, data):
        try:
            if self.check_1000():
                add_to_database(data)
            else:
                return False
        except:
            pass
        return True

    def on_error(self, status):
        tweet_tracker.apply_async((), countdown=5*60)
        print "Limit Exeeded==================>"
        return False
    #This handles Twitter authetification and the connection to Twitter Streaming API

def add_to_database(d):
    Tweet.objects.create(tweet=json.loads(d)['text'])

@task
def tweet_tracker():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['haircut'])

