import os

import requests
from dotenv import load_dotenv


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self._sheety_endpoint = os.getenv('SHEETY_ENDPOINT')
        self._sheety_token = os.getenv('SHEETY_TOKEN')
        self.SHEET_NAME = "price"
        self.sheet_headers = {
            "Authorization": f"Bearer {os.getenv('SHEETY_TOKEN')}"
        }

    def get_data(self):
        request = requests.get(url=self._sheety_endpoint, headers=self.sheet_headers)
        prices = request.json()
        return prices

    def write_data(self, city, iata_code, lowest_price):
        flight_parameters = {
            self.SHEET_NAME: {
                "city": city,
                "iataCode": iata_code,
                "lowestPrice": lowest_price
            }
        }
        print(flight_parameters)
        sheety_write = requests.post(url=self._sheety_endpoint, json=flight_parameters, headers=self.sheet_headers)
        print(sheety_write.status_code)
        print(sheety_write.json())

    def update_iata(self, id, iata_code):
        new_iata_url = f"{self._sheety_endpoint}/{id}"
        iata_parameters = {
            self.SHEET_NAME: {
                "id": id,
                "iataCode": iata_code,
            }
        }
        sheety_put = requests.put(url=new_iata_url, json=iata_parameters, headers=self.sheet_headers)
        print(sheety_put.status_code)
        print(sheety_put.json())
