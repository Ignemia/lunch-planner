from restaurants import Bruxx, NaPasece, PizzeriaEinstein, Kravin

REGISTERED_RESTAURANTS = set()

def initialize_restaurants():
    REGISTERED_RESTAURANTS.add(Bruxx())
    REGISTERED_RESTAURANTS.add(NaPasece())
    REGISTERED_RESTAURANTS.add(PizzeriaEinstein())
    REGISTERED_RESTAURANTS.add(Kravin())

if __name__ == "__main__":
    initialize_restaurants()
    for restaurant in REGISTERED_RESTAURANTS:
        restaurant.fetch_menu()
        print(f"""{restaurant.get_name()}({restaurant.get_distance()}m)<\n\t{restaurant.get_menu_string()}>""")
