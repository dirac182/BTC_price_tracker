import requests
import smtplib
from datetime import datetime, timedelta
import time
import pandas

STOCK_API_KEY = ""
NEWS_API_KEY = ""
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
    "pageSize": 2,
    "from": str(days_ago)
}

def pull_articles(tkr: str, movement: str, price: float,change: float):
    news_api = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    news_data = news_api.json()["articles"]
    for arts in news_data:
        source = arts["source"]["name"]
        date = arts["publishedAt"].split("T")[0]
        title = arts["title"]
        description = arts["description"]
        url = arts["url"]
        print("Source: " + source)
        print("Date: " + date)
        print("Title: " + title)
        print("Description: " + description)
        print("URL: " + url)
        send_notif(tkr=tkr,movem=movement,title=title,date=date,descr=description,url=url, change=change,price=price)
def send_notif(tkr: str, movem: str,title: str, date: str, descr: str, url: str, change: float, price: float):
    pass
def update_btc_data(trk: str, date: str, time: str, price: float, move: str, change: float):
    # with open(file="btc_data.csv", mode="w") as file:
    df = pandas.read_csv("btc_data.csv")
    data = {
        'Ticker': [trk],
        "Date": [date],
        "Time": [time],
        "Price": [price],
        "Movement": [move],
        "% change": [change],
    }
    new_data = pandas.DataFrame(data)
    new_data.to_csv("btc_data.csv",mode="a",index=False,header=False)
    if float(change) >= 1.5:
        pull_articles(tkr=trk, movement= move, price= price ,change= change)

old_data = pandas.read_csv("btc_data.csv")
last_row = old_data.tail(1)
last_btc_price = float(last_row["Price"])

def btc_check():
    global last_btc_price
    move: str
    stock_api = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
    btc_data = stock_api.json()
    ticker = btc_data["Realtime Currency Exchange Rate"]["1. From_Currency Code"]
    now_price = float(btc_data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    before_price = last_btc_price
    today = str(datetime.today())
    date = today.split(" ")[0]
    time = today.split(" ")[1].split(".")[0]
    if now_price/before_price > 1:
        move = "Increase"
        print("Increase")
    elif now_price/before_price < 1:
        move = "Decrease"
        print("Decrease")
    elif now_price/before_price == 1:
        move = "No Change"
        print("No Change")
    percent_change = round(abs(((now_price-before_price)/((before_price + now_price)/2))*100),6)
    if percent_change > .99999:
        pass
    update_btc_data(trk= ticker,date=date,time=time, price=now_price, move=move, change=percent_change)
    print("Current Price: " + str(now_price))
    print("Last Price: " + str(last_btc_price))



    last_btc_price = now_price

while True:
    btc_check()
    time.sleep(30)
