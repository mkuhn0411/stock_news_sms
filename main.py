import requests
import datetime as dt
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# stock api
STOCK_API = "REMOVEDFORPRIVACY"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# twilio api
account_sid = "REMOVEDFORPRIVACY"
auth_token = "REMOVEDFORPRIVACY"

# news api
NEWS_API = "REMOVEDFORPRIVACY"

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)


def send_sms(article):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=article,
        from_="REMOVEDFORPRIVACY",
        to="REMOVEDFORPRIVACY"
    )

    print(message.status)


def get_company_news(net_gain, diff_percentage):
    news_response = requests.get(url=f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={yesterday}&sortBy=popularity&apiKey={NEWS_API}")
    total_articles = news_response.json()["articles"]
    three_articles = total_articles[:3]
    icon = "⬆️" if net_gain > 0 else "⬇️"
    formatted_articles = [f"{STOCK_NAME}: {icon} {diff_percentage}% \nHeadline: {article_data['title']}. \nBrief: {article_data['description']}" for article_data in three_articles]

    for article in formatted_articles:
        send_sms(article)


def run():
    stock_response = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK_NAME}&apikey={STOCK_API}")
    data = stock_response.json()["Time Series (Daily)"]
    stock_data = [stock_info for (day, stock_info) in data.items()]

    yesterday_close = float(stock_data[0]["4. close"])
    day_before_yesterday_close = float(stock_data[1]["4. close"])
    net_gain = yesterday_close - day_before_yesterday_close

    diff_percentage = round((abs(net_gain)/yesterday_close) * 100, 2)
    diff_percentage > 1 and get_company_news(net_gain, diff_percentage)


run()
