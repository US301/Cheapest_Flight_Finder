import requests
import os

authorization = os.environ["AUTH"]


class DataManager:
    def __init__(self):
        self.api_key = os.environ['URL_SHEETS']
        self.headers = {"Authorization": authorization}

    def get_sheet_data(self):
        self.sheet_info = requests.get(url=self.api_key, headers=self.headers)
        self.sheet_info.raise_for_status()
        self.sheet = self.sheet_info.json()["prices"]
        return self.sheet

    def post_sheet_data(self, code, id):
        self.price = { "price": {"iataCode": code, }}
        self.add_code = requests.put(url=f"{self.api_key}/{id}", json=self.price, headers=self.headers)

