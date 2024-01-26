import requests
from datetime import datetime, timedelta
import config


FLIGHT_API_KEY = config.FLIGHT_API_KEY
FLIGHT_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
GBP_SIGN = "\xA3"

date = datetime.now()
# print(date)

next_day = date + timedelta(1)
six_months_date = next_day + timedelta(6*30)
# six_months_date = datetime(2024, 5, 18)

"""
This code needs refactoring, I struggled with this project to get it to work, my code is all over.
IMPORTANT: I need to learn, understand OOP, class concepts.
"""

class FlightData:
    """This class is responsible for structuring the flight data."""

    price: int
    departure_city: str
    departure_airport_code: str
    arrival_city: str
    arrival_airport_code: str
    local_departure: str
    local_arrival: str

    def flight_details(self, city_code):
        
        header = {
            "apikey": FLIGHT_API_KEY,
        }

        params = {
            "fly_from": "LON",
            "fly_to": city_code,
            "date_from": next_day.strftime("%d/%m/%Y"),
            "date_to": six_months_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
            
        }

        response = requests.get(
            url=FLIGHT_SEARCH_ENDPOINT, params=params, headers=header)
        
        try:
            self.resp = response.json()["data"][0]

        except IndexError:
            print(f"No flight found for {self.resp['route'][0]['cityTo']}")

            
        self.departure_city = self.resp["cityFrom"]
        self.departure_airport_code = self.resp["cityCodeFrom"]
        self.price = self.resp["price"]
        self.arrival_city = self.resp["cityTo"]
        self.arrival_airport_code = self.resp["cityCodeTo"]
        self.local_departure = self.resp["local_departure"]
        self.local_arrival = self.resp["local_arrival"]

        
        # self.departure_city = resp["cityFrom"]
        # self.departure_airport_code = resp["cityCodeFrom"]
        # self.price = resp["price"]
        # self.arrival_city = resp["cityTo"]
        # self.arrival_airport_code = resp["cityCodeTo"]
        # self.local_departure = resp["local_departure"]
        # self.local_arrival = resp["local_arrival"]

        #local_date_time = self.local_departure.split("T")
        #arrival_date_time = self.local_arrival.split("T")

        # testing my solution
        # data = f"From: {self.departure_city}\n \
        #       Depart Date and Time: {local_date_time[0]} - {local_date_time[1][0:-4]}\n \
        #       To: {self.arrival_city}\n \
        #       Arrival Date and Time: {arrival_date_time[0]} - {arrival_date_time[1][0:-4]}\n \
        #       Price: {GBP_SIGN}{self.price}"

        # print(data)
        price = self.price
        arrival_city = self.arrival_city
        # return f"{self.arrival_city}: £{self.price}"

        flight_info = f"{arrival_city}: £{price}"
        print(flight_info)

        return self.resp
        #return self.data


# for testing purpose

#city = FlightData()
# city.city_price()
#print(city.flight_details("PAR"))
