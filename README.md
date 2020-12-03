# Stock-Project
This document explains how the data from Twitter was collected and assigned a sentimental analysis value. If you prefer to only read the code, see [twitter_dataset.py](https://github.com/Shank4r/Stock-Project/blob/main/twitter_dataset.py)

## Installation
> pip install twitterSentiment

> pip3 install --user --upgrade git+https://github.com/yunusemrecatalcam/twint.git@twitter_legacy2

## Data Collection
Twitter is one of the biggest platforms for expressing public opinions. Every day, millions of opinions are published online and amongst these there are opinions about stocks which can influence the stock market. Our goal is to use Sentimental Analysis on these tweets to indicate if a tweet is a positive or a negative opinion. This allows us to understand the percentage of positive tweets on a particular day.

##### Note:
Data collection ranges from 01/01/2017 - 01/01/2020.

### Scraping tweets
A python module called [Twint](https://github.com/twintproject/twint) was used to scrape Tweets from Twitter. More about the module can be found [here](https://github.com/twintproject/twint). 

The code below fetches the first 100 tweets published with ```#apple``` in english.

```python
c = twint.Config()
c.Search = '"AAPL" OR "APPLE STOCK" OR "Apple Inc." OR "iphone" OR "Macbook" -eat -giveaway'
c.Limit = 100
c.Lang = 'en'
c.Since = date_index[i]
c.Until = date_index[i+1]

twint.run.Search(c)
statuses = c.search_tweet_list
```
As we are only getting the first 100 tweets between ```start_date``` and ```end_date```, we can simply run the code in a while loop and setting the interval between ```start_date``` and ```end_date``` to be one day. This way, we are able to fetch the first 100 tweets each day from 01/01/2017 and 01/01/2020

### Sentimental Analysis of tweets
[twitter-sentiment](https://github.com/TeddyCr/twitter-sentiment) is a python module which is used to classify the sentiment of a set of tweets where
* 1: positive
* 0: negative

More information about the module can be found [here](https://github.com/TeddyCr/twitter-sentiment).

#### Data manipulation
In order to use the twitter-sentimental module, every tweet from the data collection had to be manipulated as a ```dict``` with the same keys used in twitter-sentimental module. A code block from data manipulation is shown below:

```python
# for every tweet in a list of tweets (one day)
for tweet in statuses:
        tweet['id'] = tweet['data-item-id']
        tweet['full_text'] = tweet['tweet']
        tweet['created_at'] = tweet['date']
        tweet['geo'] = None
        tweet['place'] = None
        tweet['coordinates'] = None
        tweet['retweet_count'] = 0
        tweet['favorite_count'] = 0
        ...

tweets = {}
tweets['statuses'] = statuses
```

#### Sentiment classification
To get the ratio of positive tweets for one day, we use the methods specified in the [documentation](https://github.com/TeddyCr/twitter-sentiment/blob/master/doc/gettingstarted.rst) as shown in the code block below:

```python
data = twitterSentiment.StructureStatusesData(tweets)
structured_data = data.getTweet()

sentiment = twitterSentiment.SentimentScore(structured_data)
sentiment_value = sentiment.getSentimentClassification() # ratio of positively classified tweets 
return round(sentiment_value, 2) # round to two decimal
```

## Results

The ratio of positively classified tweets were combined with its corresponding day and written to a ```.csv``` file. The table below shows the first 5 days of the data collection:

Date | S/A
-----|-----
2017-01-01 | 0.67
2017-01-02 | 0.76
2017-01-03 | 0.69
2017-01-04 | 0.66
2017-01-05 | 0.64

## Improvements

### Collect more data
Currently the number of tweets acquired each day is set to 100. By increasing this to a larger integer, we are able to collect more data and a broad spectrum of opinions. As a result, it will take much longer to collect these data.

### Interpretation of emoticons in tweets
In the modern world, many uses emoticons to express their feelings and opinions. The [twitter-sentimental](https://github.com/TeddyCr/twitter-sentiment/blob/master/twitterSentiment/twitterSentiment.py) module cleans the tweet by only removing links. The classifier itself uses Naive Bayes and does not interpret the different emoticons. A suggestion would be to look at other classifiers which takes emoticons into account as well.
