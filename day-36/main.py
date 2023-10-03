import config
import os
import requests
from twilio.rest import Client

# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)

TWILIO_ACCOUNT_SID = config.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = config.TWILIO_AUTH_TOKEN

MY_ALPHA_API = config.MY_ALPHA_API
MY_NEWS_API = config.MY_NEWS_API

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# My Solution
# query_str = f"?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={MY_ALPHA_API}"
# url = STOCK_ENDPOINT+query_str
# r = requests.get(url)
# data = r.json()

data = {"function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": MY_ALPHA_API
        }

response = requests.get(STOCK_ENDPOINT, params=data)
time_series_data = response.json()["Time Series (Daily)"]
# print(time_series_data)


# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

# yesterday_stock_close = [value for (key, value) in time_series_data.items()]
# print(yesterday_stock_close[0]["4. close"])
# before_yesterday_close = [value for (key, value) in time_series_data.items()]
# print(before_yesterday_close[1]["4. close"])


for index, (key, value) in enumerate(time_series_data.items()):
    # print(index, value)
    if index == 0:
        yesterday_stock_close = float(value["4. close"])
        print("Yesterday's Close:", yesterday_stock_close)

    # TODO 2. - Get the day before yesterday's closing stock price
    if index == 1:
        before_yesterday_close = float(value["4. close"])
        print("Day Before Yesterday Close:", before_yesterday_close)


# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
stock_price_pct = abs(before_yesterday_close -
                      yesterday_stock_close) / yesterday_stock_close

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
stock_price_pct = round(float(stock_price_pct) * 100, 2)
# or
# print(f"Stock Percent Movement: {stock_price_pct:.2%}")


# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# if stock_price_pct < 5:
# print("Get News")

news_data = {"q": COMPANY_NAME,
             "searchIn": ['title', 'description', 'content'],
             "apiKey": MY_NEWS_API,
             }

res = requests.get(NEWS_ENDPOINT, params=news_data)
# print(res.url)
# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
company_news = res.json()["articles"]
# print(company_news)

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
sliced_news = company_news[0:3]

# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
articles_list = [(value["title"], value["description"])
                 for value in sliced_news]
# print(articles_list)

# TODO 9. - Send each article as a separate message via Twilio.
stock_up = "🔺"
stock_down = "🔻"

for title, desc in articles_list:
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # message_body = f"{STOCK_NAME}: 🔺{stock_price_pct}%\nHeadline: {title}\nBrief: {desc}\n"

    if stock_price_pct > 2:
        message_body = f"{STOCK_NAME}: {stock_up} {stock_price_pct}%\nHeadline: {title}\nBrief: {desc}\n"
    else:
        message_body = f"{STOCK_NAME}: {stock_down} {stock_price_pct}%\nHeadline: {title}\nBrief: {desc}\n"

    message = client.messages.create(
        body=message_body,
        from_='+13346058969',
        to='+27813791664'
    )
