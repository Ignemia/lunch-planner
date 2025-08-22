import requests
import bs4
import re

from .menicka_handler import extract_information_menicka
from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS, DISTANCE_UNITS
from models import MainMeal, Soup

class KravinMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = Kravin
        self.meals = {
            "soups": set(),
            "main_meals": set()
        }

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

class Kravin(ARestaurant):
    def __init__(self):
        ARestaurant.__init__(self, "Kravin")
        self.menu_link = "https://www.menicka.cz/2041-restaurace-kravin.html#m"
        self.distance = {
            "distance": 0,
            "units": DISTANCE_UNITS.M
        }

    def fetch_menu(self):
        assert self.menu_link != "" and self.menu_link is not None
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for Kravin")
            menu_html = rq.text
            soup_ = bs4.BeautifulSoup(menu_html, "html.parser")
            _, self.distance["distance"], menu_soup = extract_information_menicka(soup_)
            menu = self.parse_menu(menu_soup)
            self.add_menu(menu)

    def parse_menu(self, __menu_html) -> KravinMenu:
        assert __menu_html is not None and __menu_html != ""
        menu = KravinMenu()

        # Parsing soups
        soups = __menu_html.findAll(class_="polevka")
        for s_ in soups:
            price_soup = s_.find(class_="cena").text
            name = s_.find(class_="polozka").text.strip()
            soup_item = Soup(name, 0, MEAL_AMOUNT_UNITS.ML, [])
            price_czk_match = re.match(r"\d+", price_soup)
            if price_czk_match is not None:
                soup_item.set_price(int(price_czk_match[0]))
            menu.add_soup(soup_item)

        # Parsing main meals
        main_meals = __menu_html.findAll(class_="jidlo")
        for mm_ in main_meals:
            price_soup = mm_.find(class_="cena").text
            match = re.search(r"^\d+\.\s?(?P<meal_name>.*)", mm_.find(class_="polozka").text)
            if match is None:
                continue
            mm = MainMeal(match.group("meal_name"), 0, MEAL_AMOUNT_UNITS.G, [])
            price_czk_match = re.match(r"\d+", price_soup)
            if price_czk_match is not None:
                mm.set_price(int(price_czk_match[0]))
            menu.add_mainmeal(mm)

        return menu
