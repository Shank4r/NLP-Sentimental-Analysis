# Sentimental Analysis of Tweets
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

The code below fetches the first 100 tweets published in english with certain phrases and excludes keywords where ```-``` is present.

```python
c = twint.Config()
c.Search = '"Apple Inc." OR "iPad" OR "iPhone" OR "MacBook" OR "MacBook Pro" OR "MacBook Air" OR "iMac" OR "iOS" OR "ipados" OR "macos" OR "Apple-designed processors" -eat -fruit -giveaway -ebay -amazon'
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
2017-01-01 | 0.71
2017-01-02 | 0.61
2017-01-03 | 0.64
2017-01-04 | 0.69
2017-01-05 | 0.61

## Improvements

### Collecting reasonable tweets
Not all tweets with a certain phrase will influence the stock market. It is therefore important to gather tweets which has high popularity, i.e. tweets with high number of likes, retweets, replies etc. As mentioned earlier, Twint only allows to fetch n first tweets on a particular day. Thus, there will be no randomness and tweets with low popularity will not be accounted for.

### Collect more data
Currently the number of tweets acquired each day is set to 100. By increasing this to a larger integer, we are able to collect more data and a broad spectrum of opinions. As a result, it will take much longer to collect these data.

### Interpretation of emoticons in tweets
In the modern world, many uses emoticons to express their feelings and opinions. The [twitter-sentiment](https://github.com/TeddyCr/twitter-sentiment/blob/master/twitterSentiment/twitterSentiment.py) module cleans the tweet by only removing links. The classifier itself uses Naive Bayes and does not interpret the different emoticons. A suggestion would be to look at other classifiers which takes emoticons into account as well.
