# check-my-stock
Interactive dashboard with customized reports and visualizations on personal stock portfolio performance. <br>
Available at http://check-my-stock.herokuapp.com/ <br>

![picture](https://github.com/ipansh/check-my-stock/blob/main/static/example.png)

Architecture: <br>
 – **base.py** - customized api wrapper around the yahoo finance endpoint, has a range of functions related to stock price dynamics and company financial reports <br>
 – **app.py** – flask wrapper that uses base.py functions to call data, process it and visualize with plotly <br>
<br>
WARNING!<br>
Quite slow on the load since every page calls api, yet to implement the DB and caching. <br>
<br>
App deployed through Heroku. My deep appreciation for making it so user-friendly.<br>
