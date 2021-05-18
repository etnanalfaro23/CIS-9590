import re
import string
from nltk.stem.porter import PorterStemmer
import pickle

# Author Immanuel Augustine

# REFERENCE : https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags 
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def preprocess2(tweets):
    # Remove URLS and mentions @
    #tweet = re.sub(r"(?:\@|https?\://)\S+", "", tweet) 
    clean = []
    ps = PorterStemmer()
    for tweet in tweets:
            
        # Make all characters lower case
        tweet = str(tweet.lower())
        
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',str(tweet))
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        
        # Code a way to separate hashtags if together
        tweet = [char for char in tweet if char not in string.punctuation]
        tweet = ''.join(tweet)
        tweet = remove_emoji(tweet)
        
        tweet = [ps.stem(word) for word in tweet] # Stem each word
        tweet = ''.join(tweet)
        clean.append(tweet)
        
    return clean

def loadmodels():
    countvect  = pickle.load(open('models/count_vect.pkl', 'rb'))
    model = pickle.load(open('models/naive_bayes_model.pkl', 'rb'))
    return countvect, model
    


