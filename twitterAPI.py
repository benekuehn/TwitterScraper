import tweepy
import csv

# Twitter API credentials
consumer_key = ""
consumer_secret = ""

# pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

Collected_data = []

#name of twitter account
screen_name = ""

#number of tweets
tweets_max = 3000

#how many tweets per API request, default 200
tweets_per_call = 200

if tweets_max > tweets_per_call:
    new_tweets = api.user_timeline(
        screen_name=screen_name, count=tweets_per_call)

elif tweets_max < tweets_per_call:
    tweets_per_call = tweets_max
    new_tweets = api.user_timeline(
        screen_name=screen_name, count=tweets_per_call)

Collected_data.extend(new_tweets)

oldest = Collected_data[-1].id - 1

tweets_collected = tweets_per_call
tweets_needed = tweets_max - tweets_collected

while tweets_needed != 0:

    if tweets_needed < tweets_per_call:
        tweets_needed = tweets_per_call

    new_tweets = api.user_timeline(
        screen_name=screen_name, count=tweets_needed, max_id=oldest)

    tweets_needed = tweets_needed - tweets_per_call

    print(tweets_collected)

    Collected_data.extend(new_tweets)

    oldest = Collected_data[-1].id - 1

outtweets = [[tweet.id,
              tweet.user.screen_name,
              tweet.created_at,
              tweet.favorite_count,
              tweet.retweet_count,
              tweet.retweeted,
              tweet.source,
              tweet.text,
              tweet.truncated,
              tweet.in_reply_to_screen_name,] for tweet in Collected_data]

i = 0

for tweet in Collected_data:
    if "media" in tweet.entities:
        if "media" in tweet.extended_entities:
            outtweets[i].append(tweet.extended_entities["media"][0]["type"])

    i += 1


with open('tweets.csv', "w",) as f:
    writer = csv.writer(f)
    writer.writerow(["tweet_id",
                     "username",
                     "created_at",
                     "favorites",
                     "retweets",
                     "retweeted",
                     "source",
                     "text",
                     "truncated",
                     "in_reply_to_screen_name",
                     "media_type"])
    writer.writerows(outtweets)

pass
