import os

import requests
from datetime import datetime

app_ID = os.environ.get("APP_ID")
api_key = os.environ.get("API_KEY")

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
ADD_ROW_ENDPOINT = "https://api.sheety.co/5ba0f577241a78c47f8e183661d59789/workoutTracking/sheet1"

headers = {
    "Authorization": os.environ.get("AUTH"),
    "x-app-id": app_ID,
    "x-app-key": api_key,
    "Content-Type": "application/json",
    "x-remote-user-id": "0"
}

# request input from user in a natural language format
user_input = input("Tell me which exercises you did? ")

# query the server
parameters = {
    "query": user_input
}

response = requests.post(url=EXERCISE_ENDPOINT,
                         json=parameters, headers=headers)

# print(response.text)
exercises = response.json()["exercises"]

# data_list = [(value["user_input"], value["duration_min"], value["nf_calories"])
#             for value in exercises]
# print(data_list)

# Get the current date and time
today = datetime.now()
