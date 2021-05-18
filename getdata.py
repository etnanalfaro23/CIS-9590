import tweepy
import re

import pandas as pd
import datetime as dt
import yfinance as yf

from helpers import preprocess2
import requests


API_KEY='NEWSAPI_KEY'

consumer_key = 'TWITTER_CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET_KEY'

access_token = 'TWITTERACCESSTOKEN'
access_token_secret = 'ACCESSTOKENSECRET'

# Author  Immanuel Augustine
def getTweets(stockticker, stockname):
    print('Getting tweets')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search,
                       q=f'#{stockticker} OR #{stockname} -filter:retweets',
                       lang="en").items(500)
    
    tweets = [t.text for t in tweets]
    clean_text = preprocess2(tweets)
    print('Done getting tweets')
    
    return clean_text

# Author James Lee, Immanuel Augustine
def getFinanaceInfo(stockname):
    A = yf.Ticker(stockname)
    
    B = A.info

    if 'sector' in B.keys():
        B = {'longBusinessSummary': B['longBusinessSummary'],
        'sector': B['sector'],
        'previousClose': B['previousClose'],
        'marketCap': B['marketCap'],
        'fiftyTwoWeekLow': B['fiftyTwoWeekLow'],
        'profitMargins': B['profitMargins'],
        'symbol': B['symbol'],
        'sharesShort': B['sharesShort'], 
        'priceToBook': B['priceToBook'], 
        'shortRatio': B['shortRatio'], 
        'lastSplitFactor': B['lastSplitFactor']}
    else:
        B = {'previousClose': B['previousClose'],'marketCap': B['marketCap'],
    'fiftyTwoWeekLow': B['fiftyTwoWeekLow'], 'profitMargins': B['profitMargins'], 'symbol': B['symbol'],
    'sharesShort': B['sharesShort'], 'priceToBook': B['priceToBook'], 'shortRatio': B['shortRatio'], 
    'lastSplitFactor': B['lastSplitFactor']}


    #print(B)
    dataset1d = A.history(period ='1d', interval = '5m')
    #datasetidx = dataset1d.index.astype(str)
    datasetidx = dataset1d.index.time.astype(str)
    dataset1d = dataset1d['Close']
    
    data_idx_list = datasetidx.tolist()
    
    data_list = dataset1d.tolist()
    
    # dataset1d = A.history(period ='5d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')

    return B, data_list, data_idx_list

# Author James Lee, Immanuel Augustine
def getNews(stockticker, stockname):
    print(stockticker, stockname)
    url = (f'https://newsapi.org/v2/everything?q={stockname}+{stockticker}&apiKey=c9b6e4855af84dbcbe68b5d144143f6e&language=en&sortBy=publishedAt')
    

    response = requests.get(url)
    response1 = response.json()
    articles = response1['articles']
    info = {}
    for result in articles:
        info[result['url']] = result['title']    
    return info