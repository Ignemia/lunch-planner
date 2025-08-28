<<<<<<< HEAD
import argparse
from ws import start
from restaurants import Bruxx, NaPasece, PizzeriaEinstein, Kravin, Concordia, Hajnovka, MlsnejKocour, ZapomenutyCas, Parlament

def initialize_restaurants(specific_restaurant=None):
    # Initialize the concrete restaurant instances and return them
    restaurants = set()

    if specific_restaurant:
        # Use match...case to handle the specific restaurant initialization
        match specific_restaurant:
            case "Bruxx":
                restaurants.add(Bruxx.get_instance(Bruxx, "Bruxx"))
                Bruxx.get_instance(Bruxx, "Bruxx").fetch_menu()
            case "NaPasece":
                restaurants.add(NaPasece.get_instance(NaPasece, "NaPasece"))
                NaPasece.get_instance(NaPasece, "NaPasece").fetch_menu()
            case "PizzeriaEinstein":
                restaurants.add(PizzeriaEinstein.get_instance(PizzeriaEinstein, "PizzeriaEinstein"))
                PizzeriaEinstein.get_instance(PizzeriaEinstein, "PizzeriaEinstein").fetch_menu()
            case "Kravin":
                restaurants.add(Kravin.get_instance(Kravin, "Kravin"))
                Kravin.get_instance(Kravin, "Kravin").fetch_menu()
            case "Concordia":
                restaurants.add(Concordia.get_instance(Concordia, "Concordia"))
                Concordia.get_instance(Concordia, "Concordia").fetch_menu()
            case "Hajnovka":
                restaurants.add(Hajnovka.get_instance(Hajnovka, "Hajnovka"))
                Hajnovka.get_instance(Hajnovka, "Hajnovka").fetch_menu()
            case "MlsnejKocour":
                restaurants.add(MlsnejKocour.get_instance(MlsnejKocour, "MlsnejKocour"))
                MlsnejKocour.get_instance(MlsnejKocour, "MlsnejKocour").fetch_menu()
            case "ZapomenutyCas":
                restaurants.add(ZapomenutyCas.get_instance(ZapomenutyCas, "ZapomenutyCas"))
                ZapomenutyCas.get_instance(ZapomenutyCas, "ZapomenutyCas").fetch_menu()
            case "Parlament":
                restaurants.add(Parlament.get_instance(Parlament, "Parlament"))
                Parlament.get_instance(Parlament, "Parlament").fetch_menu()
    else:
        # Initialize all restaurants if no specific restaurant is specified
        restaurants.add(Bruxx.get_instance(Bruxx, "Bruxx"))
        restaurants.add(NaPasece.get_instance(NaPasece, "NaPasece"))
        restaurants.add(PizzeriaEinstein.get_instance(PizzeriaEinstein, "PizzeriaEinstein"))
        restaurants.add(Kravin.get_instance(Kravin, "Kravin"))
        restaurants.add(Concordia.get_instance(Concordia, "Concordia"))
        restaurants.add(MlsnejKocour.get_instance(MlsnejKocour, "MlsnejKocour"))
        restaurants.add(Hajnovka.get_instance(Hajnovka, "Hajnovka"))
        restaurants.add(ZapomenutyCas.get_instance(ZapomenutyCas, "ZapomenutyCas"))
        restaurants.add(Parlament.get_instance(Parlament, "Parlament"))

    return restaurants

def parse_arguments():
    parser = argparse.ArgumentParser(description="Restaurant Menu Initialization")
    parser.add_argument('-r', '--restaurant', type=str, help="Name of the specific restaurant")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Initialize restaurants based on command-line argument
    specific_restaurant = args.restaurant
    restaurants = initialize_restaurants(specific_restaurant)

    if restaurants:
        # If we have a valid restaurant or set of restaurants, print their menus
        for restaurant in restaurants:
            print(f"Restaurant: {restaurant.get_name()}")
            print(f"Menu: {restaurant.get_menu_string()}")
            print("-" * 40)

    # Pass the initialize_restaurants function to the server to start the app
    if not specific_restaurant:
        start(initialize_restaurants)  # Start the app with all restaurants
=======
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
>>>>>>> 880d2e4 (Default functionality (#2))
