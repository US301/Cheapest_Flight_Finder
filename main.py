import datetime as dt
from datetime import datetime as dtt

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

today_ = dtt.strptime(dtt.today().date().strftime("%d/%m/%Y"), "%d/%m/%Y")
next_month_ = today_ + dt.timedelta(days=(6*30))
today = today_.date().strftime("%d/%m/%Y")
next_month = next_month_.date().strftime("%d/%m/%Y")


ORIGIN_CITY_IATA = "LON"

sheet_data = DataManager()
flight_details = FlightSearch()
message = NotificationManager()
sheet_data_prices = sheet_data.get_sheet_data()


for row in sheet_data_prices:
    if not row["iataCode"]:
        city = FlightSearch(row["city"])
        city_code = city.get_code()
        sheet_data.post_sheet_data(city_code, row["id"])

for row in sheet_data_prices:
    flights = flight_details.check_flights(ORIGIN_CITY_IATA, row["iataCode"], today, next_month)
    if flights is None:
        continue
    print(flights.price)
    if row["lowestPrice"] >= flights.price:
        msg = f"Low price alert! Only ${flights.price} to fly from {flights.origin_city}-{flights.origin_airport} to {flights.destination_city}-{flights.destination_airport}, from {flights.out_date} to {flights.return_date}"
        if flights.stop_overs > 0:
            msg += f"Flight has {flights.stop_over} stop over, via {flights.via_city} city"
        send_email_message = message.send_emails(msg)
        print(send_email_message)

