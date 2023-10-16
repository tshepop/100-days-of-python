# import os
import config
import requests
from datetime import datetime

app_ID = config.APP_ID
api_key = config.API_KEY
auth = config.AUTH

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
ADD_ROW_ENDPOINT = "https://api.sheety.co/5ba0f577241a78c47f8e183661d59789/workoutTracking/sheet1"

headers = {
    "Authorization": auth,
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
# print(exercises)

# data_list = [(value["user_input"], value["duration_min"], value["nf_calories"])
#             for value in exercises]
# print(data_list)

# Get the current date and time
today = datetime.now()

# loop the list object and retrieve values to pass to request body(json),
# and save the passed values to google sheet or excel
for index, value in enumerate(exercises):

    body = {
        "sheet1": {
            "date": today.strftime("%Y%m%d"),
            "time": today.strftime("%X"),
            "exercise": str(value["user_input"]).title(),
            "duration": value["duration_min"],
            "calories": value["nf_calories"],
        }
    }

    sheet_response = requests.post(url=ADD_ROW_ENDPOINT,
                                   json=body, headers=headers)
    print(sheet_response.text)
