from flask import Flask, request, render_template
import pandas as pd
import plotly
from plotly import graph_objects as go
import base
import json
import numpy as np

from plotly.subplots import make_subplots

app = Flask(__name__)

def get_stock_data():
    main_daily_df = base.get_stock_daily_price('ABBV',30)
    my_tickers = ['EXC','BABA','JD','AMAT']

    for ticker in my_tickers:
        mini_df = base.get_stock_daily_price(ticker,30)
        main_daily_df = main_daily_df.merge(mini_df, left_on = 'date', right_on = 'date')
    
    return main_daily_df

def get_and_process_income_statement(ticker):
    data = base.get_income_statement(ticker, 4)[['quarter','revenue_billion','gross_profit_margin','net_profit_margin']]
    data.loc[:,'quarter'] = [quarter[-4:]+'Q'+quarter[0:1] for quarter in data['quarter']]
    data.loc[:,'quarter'] = pd.to_datetime(data['quarter'])
    return data

def get_balance_sheet(ticker):
    return base.get_la_ratio(ticker,4) 

def create_stock_plot(main_daily_df):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['abbv'], name='Abbvie', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['exc'], name='Exelon', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['baba'], name='Alibaba', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['jd'], name='Jindong', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=main_daily_df['date'], y=main_daily_df['amat'], name='Applied Materials', mode='lines+markers'))

    fig.update_layout(title_text = 'Daily Stock Price Changes',
                      yaxis_title = 'Stock Price ($)',
                      xaxis_title = 'Date',
                      height = 600, width = 1200,
                      font=dict(family="Gill Sans", size=16))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_income_satement_plot(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=data['quarter'], y=data['revenue_billion'],
                    text = data['revenue_billion'], textposition='outside',
                    name='Revenue($bn)'))

    fig.add_trace(go.Scatter(x=data['quarter'], y=data['net_profit_margin'],
                         name='Net Profit Margin(%)', text = [gpm*100 for gpm in data['net_profit_margin']],
                         texttemplate='%{text:.2f}', hovertemplate='%{text:.2f}'), secondary_y=True)

    fig.update_layout(title_text = 'Quarterly Income Statement',
                  xaxis_title = 'Quarter',
                  height = 600, width = 1200,
                  font=dict(family="Gill Sans", size=16))

    fig.update_xaxes(dtick="M3")
    fig.update_yaxes(range=[data['revenue_billion'].min()-data['revenue_billion'].std(),
                        data['revenue_billion'].max()+data['revenue_billion'].std()], secondary_y=False)

    fig.update_yaxes(range=[data['net_profit_margin'].min()-data['net_profit_margin'].std(),
                        data['net_profit_margin'].max()+data['net_profit_margin'].std()], secondary_y=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_balance_sheet_plot(data):
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=data['quarter'], y=data['assets_billion'],
                        text = data['assets_billion'], texttemplate='%{text:.1f}',
                        textposition='outside',name='Assets($bn)'))

    fig.add_trace(go.Bar(x=data['quarter'], y=data['liabilities_billion'],
                    text = data['liabilities_billion'], texttemplate='%{text:.1f}',
                    textposition='outside', name='Liabilities($bn)'))

    fig.add_trace(go.Scatter(x=data['quarter'], y=data['la_ratio'],
                            name='LA Ratio(%)', text = [la_ratio*100 for la_ratio in data['la_ratio']],
                            texttemplate='%{text:.1f}', hovertemplate='%{text:.2f}'), secondary_y=True)

    fig.update_layout(title_text = 'Quarterly Balance Sheet',
                    xaxis_title = 'Quarter',
                    height = 600, width = 1200,
                    font=dict(family="Gill Sans", size=16))

    fig.update_xaxes(dtick="M3")

    fig.update_yaxes(range=[0, data['assets_billion'].max()+data['assets_billion'].std()*3], secondary_y=False)

    fig.update_yaxes(range=[data['la_ratio'].min()-data['la_ratio'].std(),
                            data['la_ratio'].max()+data['la_ratio'].std()], secondary_y=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route("/")
def home():
    main_daily_df = get_stock_data()
    bar = create_stock_plot(main_daily_df)
    return render_template('stock_prices.html', plot=bar)

@app.route("/stock_prices")
def stock_prices_page():
    main_daily_df = get_stock_data()
    bar = create_stock_plot(main_daily_df)
    return render_template('stock_prices.html', plot=bar)

@app.route("/income_statement")
def income_statement_page():
    main_df = get_and_process_income_statement('MSFT')
    bar = create_income_satement_plot(main_df)
    return render_template('income_statement.html', plot=bar)

@app.route("/balance_sheet")
def balance_sheet_page():
    main_df = get_balance_sheet('MSFT')
    bar = create_balance_sheet_plot(main_df)
    return render_template('balance_sheet.html', plot=bar)

@app.route("/balance_sheet/company", methods = ['POST'])
def balance_sheet_page():
    message = [item for item in request.form.values()][0]
    main_df = get_balance_sheet(message)
    bar = create_balance_sheet_plot(main_df)
    return render_template('balance_sheet.html', plot=bar)

if __name__  == '__main__': 
    app.run(debug=True)