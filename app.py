from flask import Flask, render_template, request
from getdata import getTweets, getFinanaceInfo
from helpers import loadmodels
from processdata import processSentiment, processwordcloud


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/etnan', methods=['GET', 'POST'])
def etnan():
    val = request.form['searchval']
    data = getTweets(val)
    countvect, model = loadmodels()
    financedata, graphdata, timestamps = getFinanaceInfo(val)
    pos_percentage, neg_percentage = processSentiment(data, countvect, model)
    wordfrequency = processwordcloud(data)
    return render_template('Info_page.html', financedata = financedata, 
                    pos_percentage = pos_percentage, 
                    neg_percentage = neg_percentage,
                    val = val,
                    timestamps = timestamps,
                    data = graphdata,
                    wordfrequency = wordfrequency
                     )


if __name__ == '__main__':
    app.run(debug=True)
