import os
import requests
from dotenv import load_dotenv


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv('AMADEUS_API_KEY')
        self._api_secret = os.getenv('AMADEUS_API_SECRET')
        self._base_endpoint = os.getenv('AMADEUS_BASE_ENDPOINT')
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=os.getenv('AMADEUS_OAUTH2_ENDPOINT'), headers=header, data=body)
        if int(response.status_code) == 200:
            print("Got new token")

        return response.json()['access_token']

    def get_city_code(self, city):
        cities = f"{self._base_endpoint}/v1/reference-data/locations/cities"
        print(cities)
        print(self._token)
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        print(header)
        query = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS",
        }
        print(query)
        response = requests.get(url=cities, params=query, headers=header)
        print(response)
        code = response.json()['data'][0]['iataCode']
        return code

    def search_flight(self, origin_city_code, destination_city_code, initial_date, final_date):
        search_endpoint = f"{self._base_endpoint}/v2/shopping/flight-offers"
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": initial_date.strftime("%Y-%m-%d"),
            "returnDate": final_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "USD",
            "max": "2",
        }
        response = requests.get(url=search_endpoint, params=query, headers=header)

        return response.json()
