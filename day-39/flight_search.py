import requests
import config

FLIGHT_API_KEY = config.FLIGHT_API_KEY
FLIGHT_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"

"""
# date = datetime.now()
# print(date)
# date.strftime("%d,%m,%Y")

# next_day = date + timedelta(1)
# six_months_date = datetime(2023, 11, 4)
"""

header = {
    "apikey": FLIGHT_API_KEY,
}


class FlightSearch:

    def display_name(self, city_name):
        params = {
            "term": city_name
        }

        response = requests.get(
            url=FLIGHT_SEARCH_ENDPOINT, params=params, headers=header)
        location_code = response.json()["locations"][0]["code"]
        # print(location_code)
        return location_code
