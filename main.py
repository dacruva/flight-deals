# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint


data_manager = DataManager()
sheet_data = data_manager.get_data()
#send_prices = prices_rw.write_data("Paris", "12312", 2)
#print(sheet_data)

for data in sheet_data['prices']:
    row_id = data['id']
    city = data['city']
    print(row_id)
    if len(data['iataCode']) == 0:
        new_iata_code = FlightSearch().get_city_code(city)
        print(new_iata_code)
        data_manager.update_iata(row_id, new_iata_code)
