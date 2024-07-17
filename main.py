# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
import time
from flight_data import find_cheapest_flight


# Setup Flight search
data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()
DEPARTURE_IATA_CODE = "NYC"

# Update city codes in Google Sheet
for data in sheet_data['prices']:
    row_id = data['id']
    city = data['city']
    print(row_id)
    if len(data['iataCode']) == 0:
        new_iata_code = flight_search.get_city_code(city)
        print(new_iata_code)
        data_manager.update_iata(row_id, new_iata_code)
    # Slowing down requests to avoid rate limit
    time.sleep(2)

# Setting dates rage
tomorrow_date = datetime.now() + timedelta(days=1)
six_months_date = datetime.now() + timedelta(days=180)

for destination in sheet_data['prices']:
    print(f"Getting flights for {destination['city']}...")
    # getting json response with th flight information
    flights = flight_search.search_flight(
        DEPARTURE_IATA_CODE,
        destination["iataCode"],
        initial_date=tomorrow_date,
        final_date=six_months_date
    )
    # Parsing json
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)
