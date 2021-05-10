import tweepy
import pandas as pd
import re
from helpers import preprocess2
import yfinance as yf

consumer_key = 'VnpVUn3nwoecupySj6LuhZW1I'
consumer_secret = 'APBWUHCfP1OziQmDw7YpS17As8yJJerFuns9QlDxSD1WvEAXuF'

access_token = '1304641763970355200-JHeprPra1EXC8LoZVE5xUaCSALHbNK'
access_token_secret = 'Df4E8PwDPcbx97MM1SJW0r9H1HROEXWgdEOzLDtFlXm6Y'

def getTweets(stockname):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search,
                       q=f'{stockname} -rt',
                       lang="en").items(100)
    
    tweets = [t.text for t in tweets]
    clean_text = preprocess2(tweets)
    
    return clean_text

def getFinanaceInfo(stockname):
    A = yf.Ticker(stockname)
    B = A.info
    B = {'sector': B['sector'],'previousClose': B['previousClose'],'marketCap': B['marketCap'],
        'fiftyTwoWeekLow': B['fiftyTwoWeekLow'], 'profitMargins': B['profitMargins'], 'symbol': B['symbol'],
        'sharesShort': B['sharesShort'], 'priceToBook': B['priceToBook'], 'shortRatio': B['shortRatio'], 
        'lastSplitFactor': B['lastSplitFactor']}
    print(B)
    dataset1d = A.history(period ='1d', interval = '15m')
    datasetidx = dataset1d.index.astype(str)
    dataset1d = dataset1d['Close']
    
    data_idx_list = datasetidx.tolist()
    data_list = dataset1d.tolist()
    
    # dataset1d = A.history(period ='5d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')
    # dataset1d = A.history(period ='1d', interval = '60m')

    return B, data_list, data_idx_list
