# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint


prices_rw = DataManager()
#prices = prices_rw.get_data()
send_prices = prices_rw.write_data("Paris", "12312", 2)
pprint(send_prices)
