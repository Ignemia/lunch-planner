# main.py
from ws import start
from restaurants import Bruxx, NaPasece, PizzeriaEinstein, Kravin, Concordia

def initialize_restaurants():
    # Initialize the concrete restaurant instances and return them
    restaurants = set()
    restaurants.add(Bruxx.get_instance(Bruxx, "Bruxx"))
    restaurants.add(NaPasece.get_instance(NaPasece, "NaPasece"))
    restaurants.add(PizzeriaEinstein.get_instance(PizzeriaEinstein, "PizzeriaEinstein"))
    restaurants.add(Kravin.get_instance(Kravin, "Kravin"))
    restaurants.add(Concordia.get_instance(Concordia, "Concordia"))

    return restaurants

if __name__ == "__main__":
    # Pass the initialize_restaurants function to the server to start the app
    start(initialize_restaurants)
