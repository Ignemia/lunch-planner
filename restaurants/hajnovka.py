import requests
import bs4
import re
from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS, DISTANCE_UNITS
from models import MainMeal, Soup, Drink

class HajnovkaMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = Hajnovka
        self.meals = {
            "soups": set(),
            "main_meals": set(),
        }
        self.drinks = set()

    def add_soup(self, soup: AMeal) -> bool:
        try:
            self.meals["soups"].add(soup)
            return True
        except:
            return False

    def add_mainmeal(self, meal: AMeal) -> bool:
        try:
            self.meals["main_meals"].add(meal)
            return True
        except:
            return False

    def add_drink(self, name: str, volume: float, price_czk: int) -> bool:
        try:
            self.drinks.add(Drink(name, volume, price_czk))
            return True
        except:
            return False

class Hajnovka(ARestaurant):
    def __init__(self):
        ARestaurant.__init__(self, "Hajnovka")
        self.menu_link = "https://www.hajnovka.cz/denni-menu/"
        self.distance = {
            "distance": 0,
            "units": DISTANCE_UNITS.M
        }

    def fetch_menu(self):
        assert self.menu_link != "" and self.menu_link is not None
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for Hajnovka")
            menu_html = rq.text
            soup_ = bs4.BeautifulSoup(menu_html, "html.parser")
            menu_soup = soup_.find(id="denni-menu")
            if menu_soup is None:
                print("Menu soup is None")
                return
            menu = self.parse_menu(menu_soup)
            self.add_menu(menu)

    def parse_menu(self, __menu_html) -> HajnovkaMenu:
        assert __menu_html is not None and __menu_html != ""
        menu = HajnovkaMenu()

        meal_containers = __menu_html.findAll(class_="layout-restaurant_category_l")
        # Parsing Soups
        soup_container = meal_containers[0]
        soups = soup_container.find_all("div", class_="menu-item")
        for s_ in soups:
            price_html = s_.find("span", class_="price").text.strip()
            soup_name = s_.find(class_="title").text.strip()
            soup_name = soup_name.replace(price_html, "")
            description = s_.find("p").text.strip()

            price_czk_match = re.match(r"(\d+)", price_html)
            if price_czk_match:
                price_czk = int(price_czk_match.group(1))
                soup_item = Soup(soup_name, 0, MEAL_AMOUNT_UNITS.ML, [])
                soup_item.set_price(price_czk)
                soup_item.set_detailed_description(description)
                menu.add_soup(soup_item)

        # Parsing Main Meals
        main_meals_container = meal_containers[1]
        main_meals = main_meals_container.find_all("div", class_="menu-item")
        for mm_ in main_meals:
            price_html = mm_.find("span", class_="price").text.strip()
            main_meal_name = mm_.find(class_="title").text.strip()
            main_meal_name = main_meal_name.replace(price_html, "")
            description = mm_.find("p").text.strip()

            price_czk_match = re.match(r"(\d+)", price_html)
            if price_czk_match:
                price_czk = int(price_czk_match.group(1))
                main_meal_item = MainMeal(main_meal_name, 0, MEAL_AMOUNT_UNITS.ML, [])
                main_meal_item.set_price(price_czk)
                main_meal_item.set_detailed_description(description)
                menu.add_mainmeal(main_meal_item)

        return menu
