import yfinance as yf

def check_vitals(company_name):
    stock_ticker = yf.Ticker(company_name)
    stock_info = stock_ticker.info
    price = stock_info['regularMarketOpen']
    name = stock_info['shortName']
    print("The Market Open Price today for {} is ${}.".format(name, price))
