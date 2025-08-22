from restaurants import Bruxx

REGISTERED_RESTAURANTS = set()

def initialize_restaurants():
    REGISTERED_RESTAURANTS.add(Bruxx())

if __name__ == "__main__":
    initialize_restaurants()
    for restaurant in REGISTERED_RESTAURANTS:
        restaurant.fetch_menu()
        print(f"""{restaurant.get_name()}({restaurant.get_distance()}m)<\n\t{restaurant.get_menu_string()}>""")
