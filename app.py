from flask import Flask, request, render_template

import pandas as pd
pd.options.mode.chained_assignment = None
pd.set_option('display.float_format', lambda x: '%.1f' % x)

from plotly import graph_objects as go

import base

import os

app = Flask(__name__)

@app.route("/")
def home():
    print('Hello!')

"""
KEY = os.environ['rapidapi_key']

#with open('/Users/ilya/Desktop/keys/yahoo_finance.txt','r') as file:
#    key = file.readlines()

#KEY = key[0]

@app.route("/")
def home():
    main_daily_df = base.get_stock_daily_price('ABBV',30)
    my_tickers = ['EXC','BABA','JD','AMAT']

    for ticker in my_tickers:
        mini_df = base.get_stock_daily_price(ticker,30)
        main_daily_df = main_daily_df.merge(mini_df, left_on = 'date', right_on = 'date')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['abbv'], name='abbv_%', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['exc'], name='exc_%', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['baba'], name='baba_%', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['jd'], name='jd_%', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['amat'], name='amat_%', mode='lines+markers'))

    fig.update_layout(title_text = 'Daily Stock Price Changes',
                  yaxis_title = 'Stock Price',
                  xaxis_title = 'Date',
                  height = 600, width = 1200)

    fig.write_html('templates/plotly_page.html', full_html=False, include_plotlyjs='cdn')

    return render_template('plotly_page.html') 
"""

if __name__  == '__main__': 
    app.run(debug=True)