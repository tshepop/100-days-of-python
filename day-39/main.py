from data_manager import DataManager
from notification_manager import NotificationManager
from datetime import datetime, timedelta

flight_notification = NotificationManager()
data_manager = DataManager()

# pass data from prices to the variable
sheet_data = data_manager.get_travel_data()

# print(sheet_data)
# airport_code = [value['iataCode'] for value in sheet_data]
# print(airport_code)

for row in sheet_data:
    if row["iataCode"] == "":
        from flight_search import FlightSearch
        flight_data = FlightSearch()
        row["iataCode"] = flight_data.display_name(row["city"])


# print("Sheet data:\n\n", sheet_data)
# save the returned sheet_data to the data_manager dict then update the google sheet or excel
# data_manager.travel_dest_dict = sheet_data
# data_manager.update_travel_sheet()

today = datetime.now() + timedelta(1)
six_months = today + timedelta(6*30)

data = {}
if sheet_data[0]["iataCode"] != "":
    from flight_data import FlightData
    flight_data = FlightData()
    for row in sheet_data:
        data = flight_data.flight_details(row["iataCode"])
        # print(f"{data['cityTo']}: £{data['price']}")
       # data

        if data["price"] < row["lowestPrice"]:
            local_departure = data["local_departure"]
            local_arrival = data["local_arrival"]
            local_departure = local_departure.split("T")[0]
            local_arrival = local_arrival.split("T")[0]

            flight_notification.send_notification(
                message = f"Low price alert! Only £{data['price']} to fly from {data['cityFrom']}-{data['cityCodeFrom']} to {data['cityTo']}-{data['cityCodeTo']}, from {today.strftime('%d%m%Y')} to {six_months.strftime('%d%m%Y')}.")
            # print(sms)
