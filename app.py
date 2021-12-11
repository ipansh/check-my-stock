from flask import Flask, request, render_template
import pandas as pd
import plotly
from plotly import graph_objects as go
import base
import json
import numpy as np

app = Flask(__name__)

#@app.route("/")
#def home():
#    return 'Hello!'

def get_stock_data():
    main_daily_df = base.get_stock_daily_price('ABBV',30)
    my_tickers = ['EXC','BABA','JD','AMAT']

    for ticker in my_tickers:
        mini_df = base.get_stock_daily_price(ticker,30)
        main_daily_df = main_daily_df.merge(mini_df, left_on = 'date', right_on = 'date')
    
    return main_daily_df

def create_plot(main_daily_df):

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

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/")
def home():
    
    main_daily_df = get_stock_data()

    bar = create_plot(main_daily_df)

    return render_template('plotly_page.html', plot=bar) 

if __name__  == '__main__': 
    app.run(debug=True)