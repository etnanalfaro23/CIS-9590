from flask import Flask, render_template, request
from getdata import getTweets, getFinanaceInfo, getNews
from helpers import loadmodels
from processdata import processSentiment, processwordcloud
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import SelectField, validators, RadioField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR SECRET KEY'

@app.route("/" , methods = ['GET', 'POST'])
def home():
    form = ReusableForm(request.form)
    return render_template('index.html', form=form)

@app.route('/etnan', methods=['GET', 'POST'])
def etnan():
    val = request.form['searchval']
    stock_name = df.loc[df["Stock Ticker"]==val, 'Company'].item().strip()

    print(stock_name)
    data = getTweets(val, stock_name)
    #print(len(data))
    countvect, model = loadmodels()
    headlines= getNews(val, stock_name)
    #print(headlines)
    financedata, graphdata, timestamps = getFinanaceInfo(val)
    pos_percentage, neg_percentage = processSentiment(data, countvect, model)
    wordfrequency = processwordcloud(data,val)
    #newsfrequency = processwordcloud(news_text,val)
    return render_template('Info_page.html', financedata = financedata,
                    pos_percentage = pos_percentage,
                    neg_percentage = neg_percentage,
                    val = val,
                    timestamps = timestamps,
                    data = graphdata,
                    wordfrequency = wordfrequency,
                    headlines = headlines
                    #newsfrequency =newsfrequency

                     )

df = pd.read_excel("dataset.xlsx")

def getCompanies():
    stockticker = df["Stock Ticker"]
    company = df["Company"]
    results = dict(zip(stockticker, company))

    return results

class ReusableForm(FlaskForm):
    companies = getCompanies()
    name = SelectField("Enter a Ticker",
                       choices=[(ticker, name) for ticker, name in companies.items()], validators=[validators.InputRequired()])

if __name__ == '__main__':
    app.run(debug=True)
