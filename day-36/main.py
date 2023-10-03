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
