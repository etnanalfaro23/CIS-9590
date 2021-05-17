import tweepy
import re

import pandas as pd
import datetime as dt
import yfinance as yf

from helpers import preprocess2
import requests


API_KEY='c9b6e4855af84dbcbe68b5d144143f6e'

consumer_key = 'VnpVUn3nwoecupySj6LuhZW1I'
consumer_secret = 'APBWUHCfP1OziQmDw7YpS17As8yJJerFuns9QlDxSD1WvEAXuF'

access_token = '1304641763970355200-JHeprPra1EXC8LoZVE5xUaCSALHbNK'
access_token_secret = 'Df4E8PwDPcbx97MM1SJW0r9H1HROEXWgdEOzLDtFlXm6Y'

def getTweets(stockticker, stockname):
    print('Getting tweets')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search,
                       q=f'#{stockticker} OR #{stockname} -filter:retweets',
                       lang="en").items(200)
    
    tweets = [t.text for t in tweets]
    clean_text = preprocess2(tweets)
    print('Done getting tweets')
    
    return clean_text

def getFinanaceInfo(stockname):
    A = yf.Ticker(stockname)
    
    B = A.info

    if 'sector' in B.keys():
        B = {'longBusinessSummary': B['longBusinessSummary'],'sector': B['sector'],'previousClose': B['previousClose'],'marketCap': B['marketCap'],
    'fiftyTwoWeekLow': B['fiftyTwoWeekLow'], 'profitMargins': B['profitMargins'], 'symbol': B['symbol'],
    'sharesShort': B['sharesShort'], 'priceToBook': B['priceToBook'], 'shortRatio': B['shortRatio'], 
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

def getNews(stockticker, stockname):
    url = (f'https://newsapi.org/v2/top-headlines?q={stockname}&apiKey=c9b6e4855af84dbcbe68b5d144143f6e')

    response = requests.get(url)
    response1 = response.json()
    articles = response1['articles']
    # title = []
    # url = []
    info = {}
    for result in articles:
        # title.append(result['title'])
        # url.append(result['url'])
        #print(result['content'])
        info[result['url']] = result['title']



    return info