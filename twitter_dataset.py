import pandas as pd
import twint, twitterSentiment, csv

def get_sentiment_value(statuses):
    for tweet in statuses:
        tweet['id'] = tweet['data-item-id']
        tweet['full_text'] = tweet['tweet']
        tweet['created_at'] = tweet['date']
        tweet['geo'] = None
        tweet['place'] = None
        tweet['coordinates'] = None
        tweet['retweet_count'] = 0
        tweet['favorite_count'] = 0

        tweet['entities'] = {}
        tweet['entities']['hashtags'] = 0
        tweet['entities']['user_mentions'] = []

        tweet['metadata'] = {}
        tweet['metadata']['iso_language_code'] = 0
        tweet['user'] = {}
        tweet['user']['id'] = 0
        tweet['user']['name'] = ""
        tweet['user']["screen_name"] = ""
        tweet['user']["location"] = ""
        tweet['user']["description"] = ""
        tweet['user']["followers_count"] = ""
        tweet['user']["friends_count"] = ""
        tweet['user']["listed_count"] = ""
        tweet['user']["favourites_count"] = ""
        tweet['user']["verified"] = ""
        tweet['user']["statuses_count"] = ""
        tweet['user']["lang"] = ""

    tweets = {}
    tweets['statuses'] = statuses
    data = twitterSentiment.StructureStatusesData(tweets)
    structured_data = data.getTweet()

    sentiment = twitterSentiment.SentimentScore(structured_data)
    sentiment_value = sentiment.getSentimentClassification()
    return round(sentiment_value, 2)


def fetch_data(startdate, enddate):
    date_index = pd.date_range(start=startdate, end=enddate)
    date_index = date_index.format(formatter = lambda x: x.strftime('%Y-%m-%d'))
    sentimental_value_list = []
    i = 0
    while i < len(date_index) - 1:
        c = twint.Config()
        c.Search = '"AAPL" OR "APPLE STOCK" OR "Apple Inc." OR "iphone" OR "Macbook" -eat -giveaway'
        c.Limit = 100
        c.Lang = 'en'
        c.Since = date_index[i]
        c.Until = date_index[i+1]

        twint.run.Search(c)
        statuses = c.search_tweet_list
        sentiment_value = get_sentiment_value(statuses)
        sentimental_value_list.append(sentiment_value)
        print(date_index[i])
        i += 1


    rows = zip(date_index, sentimental_value_list)
    with open('twitter_dataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

# date format: month/day/year
# fetch_data('1/1/2017', '1/1/2020')