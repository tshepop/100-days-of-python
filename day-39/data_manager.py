import requests
import pprint
import config

SHEETY_API_ENDPOINT = "https://api.sheety.co/5ba0f577241a78c47f8e183661d59789/flightDeals/prices"
AUTH_HEADER = {"Authorization": config.AUTH}


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self) -> None:
        self.travel_dest_dict = {}
        # self.update = self.update_sheet()
        # self.sheet = self.getSheet()
        # self.getSheet()

    def get_travel_data(self):
        response = requests.get(
            url=SHEETY_API_ENDPOINT, headers=AUTH_HEADER)
        travel_data = response.json()["prices"]
        # pprint.pprint(travel_data)
        # self.travel_dest_dict = travel_data
        # return self.travel_dest
        return travel_data

    def update_travel_sheet(self):
        """
        This function updates the Google sheet column.
        """

        for value in self.travel_dest_dict:
            update_info = {
                "price": {
                    "iataCode": value["iataCode"],
                }
            }

            response = requests.put(
                url=f"{SHEETY_API_ENDPOINT}/{value['id']}", json=update_info, headers=AUTH_HEADER)
            print(response.text)


# data = DataManager()
# print(data.sheet)
# data.get_travel_data()
# data.update

