from django.shortcuts import render
from django.http import HttpResponse
from coreapp.tasks import tweet_tracker
from coreapp.models import Tweet
from collections import Counter
import re
import enchant

# Create your views here.
def tweets(request):
    tweet_tracker.delay()
    return HttpResponse("Tweets will be tracked from now")

def most_used(request):
    string = ""
    for i in  Tweet.objects.all():
        string+=i.tweet
    word_list = re.findall('\w+',string)
    c = Counter(word_list)
    d = enchant.Dict("en_US")
    for i in c.most_common():
        if d.check(i[0]):
            continue
        elif i[0][0].isupper():
            return HttpResponse(i[0])
        else:
            continue
    return HttpResponse("No such word")

