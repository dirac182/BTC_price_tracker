import requests
import smtplib
from datetime import datetime, timedelta
import time
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "FRAFWH3EMSX43KGQ"
NEWS_API_KEY = "ff88c467557b44b29427df585bc71399"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

today = datetime.today()
days_ago = today - timedelta(days=3)

STOCK_PARAMS = {
    "function": "CURRENCY_EXCHANGE_RATE",
    "from_currency": "BTC",
    "to_currency": "USD",
    "apikey": STOCK_API_KEY
}
NEWS_PARAMS = {
    "q": "bitcoin",
    "apiKey": NEWS_API_KEY,
    "sortBy": "relevancy",
    "pageSize": 5,
    "from": str(days_ago)
}

news_api= requests.get(url=NEWS_ENDPOINT,params=NEWS_PARAMS)
news_data= news_api.json()["articles"]

def pull_articles():
    for arts in news_data:
        source = arts["source"]["name"]
        date = arts["publishedAt"].split("T")[0]
        title = arts["title"]
        url = arts["url"]
        print("Source: " + source)
        print("Date: " + date)
        print("Title: " + title)
        print("URL: " + url)

def send_notification():
    smtp = smtplib.SMTP()

last_btc_price = 1

def btc_check():
    global last_btc_price
    stock_api = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
    btc_data = stock_api.json()
    now = float(btc_data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    before = last_btc_price
    if now/before > 1:
        print("Increase")
    elif now/before < 1:
        print("Decrease")
    elif now/before == 1:
        print("Stayed the same")
    percent_change = abs((now-before)/before)
    if percent_change > .99999:
        send_notification()
    print("Current Price: " + str(now))
    print("Last Price: " + str(last_btc_price))
    last_btc_price = now

while True:
    btc_check()
    time.sleep(60*15)

#print(btc_price)