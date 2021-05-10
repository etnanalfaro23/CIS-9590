import pandas as pd

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
    return pos_percentage, neg_percentage

def processfinancialCharts(data):
    pass

def processwordcloud(textdata):
    # Convert all lists into one string
    str1 = " " 
    test = str1.join(textdata)

    # Break up all words into unique characters
    str_list = test.split()
    unique_words = set(str_list)

    # Get word counts for each word
    word = []
    for unique in unique_words:
        word.append([unique, str_list.count(unique)])

    jsonlist = pd.DataFrame(word, columns=('x','value')).to_json(orient="records")

    return jsonlist



