# check-my-stock
Interactive dashboard with customized reports and visualizations on personal stock portfolio performance. <br>
Available at http://check-my-stock.herokuapp.com/ <br>

Architecture:
 – **base.py** - customized api wrapper around the yahoo finance endpoint, has a range of functions related to stock price dynamics and company financial reports
 – **app.py** – flask wrapper that uses base.py functions to call data, process it and visualize with plotly.
 
WARNING!
Quite slow on the load since every page calls api, yet to implement the DB and caching. 

App deployed through Heroku. My appreciation to them for making it so user-friendly.
