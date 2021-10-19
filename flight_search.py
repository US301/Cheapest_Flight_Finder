import requests
import os
from flight_data import FlightData

api_key = os.environ['API_FLIGHT']
headers = {"apikey": api_key}

url = os.environ['URL_FLIGHT_SEARCH']
flight_url = "https://tequila-api.kiwi.com/v2/search"


class FlightSearch:
    def get_code(self, city_name):
        parameters = {"term": city_name}
        code_info = requests.get(url=url, params=parameters, headers=headers)
        code_info.raise_for_status()
        code = code_info.json()
        city_code = code["locations"][0]["code"]
        return city_code

    def check_flights(self, departure_airport_code, destination_airport_code, today, next_month):
        parameters = {"fly_from": departure_airport_code,
                           "fly_to": destination_airport_code,
                           "date_from": today,
                           "date_to": next_month,
                           "nights_in_dst_from": 7,
                           "nights_in_dst_to": 28,
                           "flight_type": "round",
                           "curr": "GBP",
                           "max_stopover": 0,
                           }
        flight_info = requests.get(url=flight_url, params=parameters, headers=headers)
        try:
            json_flight = flight_info.json()["data"][0]
        except IndexError:
            parameters["max_stopover"] = 1
            flight_info = requests.get(url=flight_url, params=parameters, headers=headers)
            try:
                json_flight = flight_info.json()["data"][0]
            except IndexError:
                return None
            else:
            # json_flight = flight_info.json()["data"][0]
            # print(json_flight)
                flight = FlightData(
                    price=json_flight["price"],
                    origin_city=json_flight["route"][0]["cityFrom"],
                    origin_airport=json_flight["route"][0]["flyFrom"],
                    destination_city=json_flight["route"][1]["cityTo"],
                    destination_airport=json_flight["route"][1]["flyTo"],
                    out_date=json_flight["route"][0]["local_departure"].split("T")[0],
                    return_date=json_flight["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=json_flight["route"][0]["cityTo"],
                )
                return flight
        else:
            flight = FlightData(
                price=json_flight["price"],
                origin_city=json_flight["route"][0]["cityFrom"],
                origin_airport=json_flight["route"][0]["flyFrom"],
                destination_city=json_flight["route"][0]["cityTo"],
                destination_airport=json_flight["route"][0]["flyTo"],
                out_date=json_flight["route"][0]["local_departure"].split("T")[0],
                return_date=json_flight["route"][1]["local_departure"].split("T")[0],
            )
            return flight