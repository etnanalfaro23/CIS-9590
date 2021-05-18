from flask import Flask, render_template, request
from getdata import getTweets, getFinanaceInfo, getNews
from helpers import loadmodels
from processdata import processSentiment, processwordcloud
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import SelectField, validators


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR SECRET KEY'

# Author:Etnan Alfaro
@app.route("/" , methods = ['GET', 'POST'])
def home():
    form = ReusableForm(request.form)
    return render_template('index.html', form=form)

# Author:Etnan Alfaro, Immanuel Augustine, James Lee, Matthew Salazar
@app.route('/etnan', methods=['GET', 'POST'])
def etnan():
    # Get stock name and stock ticker
    val = request.form['searchval']
    stock_name = df.loc[df["Stock Ticker"]==val, 'Company'].item().strip()

    print(stock_name)
    # Call function to get Tweets
    data = getTweets(val, stock_name)
    #print(len(data))

    # Call function to load models
    countvect, model = loadmodels()

    # Call function to load news
    headlines= getNews(val, stock_name)
    #print(headlines)

    # Call function to get finnance data
    financedata, graphdata, timestamps = getFinanaceInfo(val)

    # Call function to process sentiment
    pos_percentage, neg_percentage = processSentiment(data, countvect, model)

    # Call function to process wordcloud
    wordfrequency = processwordcloud(data,val)


    # Render all the data returned by the function to the HTML page
    return render_template('Info_page.html', financedata = financedata,
                    pos_percentage = pos_percentage,
                    neg_percentage = neg_percentage,
                    val = val,
                    timestamps = timestamps,
                    data = graphdata,
                    wordfrequency = wordfrequency,
                    headlines = headlines)

# Author:Etnan Alfaro
df = pd.read_excel("dataset.xlsx")

# Author:Etnan Alfaro
def getCompanies():
    stockticker = df["Stock Ticker"]
    company = df["Company"]
    results = dict(zip(stockticker, company))

    return results

# Author:Etnan Alfaro
class ReusableForm(FlaskForm):
    companies = getCompanies()
    name = SelectField("Enter a Ticker",
                       choices=[(ticker, name) for ticker, name in companies.items()], validators=[validators.InputRequired()])

# Author:Etnan Alfaro
if __name__ == '__main__':
    app.run(debug=True)
