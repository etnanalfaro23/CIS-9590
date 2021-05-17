import pandas as pd

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


def processSentiment(clean_text, count_vect, model):
    count = len(clean_text)
    pos = 0
    neg = 0
    for text in clean_text:
        text = [text]
        text = count_vect.transform(text)
        result = model.predict(text)
        if result == 4:
            pos += 1
        elif result == 0:
            neg += 1
    pos_percentage = (pos/count) * 100
    neg_percentage = (neg/count) * 100
    return format(pos_percentage, '.2f'), format(neg_percentage, '.2f')

def processfinancialCharts(data):
    pass

def processwordcloud(textdata,val):
    # Convert all lists into one string
    str1 = " " 
    test = str1.join(textdata)

    # Break up all words into unique characters
    str_list = test.split()
    unique_words = set(str_list)
    

    unique_words2 = [t for t in unique_words if t not in ['atuser','url'] and t not in [val]]
    unique_words2 = [t for t in unique_words2 if t not in STOPWORDS]
    print('from wordcloud', val, len(unique_words2))

    # Get word counts for each word
    word = []
    for unique in unique_words2:
        word.append([unique, str_list.count(unique)])

    
    sorted = pd.DataFrame(word, columns=('x','value')).sort_values(by=['value'], ascending=False)
    length = int(len(sorted)*0.8)
    if length<500:
        jsonlist = sorted[:length].to_json(orient="records")
    else:
        jsonlist = sorted.to_json(orient="records")

    

    return jsonlist



