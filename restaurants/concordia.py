import requests
import bs4
import re

from .menicka_handler import extract_information_menicka
from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS, DISTANCE_UNITS
from models import MainMeal, Soup, Drink

class ConcordiaMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = Concordia
        self.meals = {
            "soups": set(),
            "main_meals": set()
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
    def add_drink(self, name:str, volume:float, price_czk: int) -> bool:
        try:
            self.drinks.add(Drink(name, volume, price_czk))
            return True
        except:
            return False

class Concordia(ARestaurant):
    def __init__(self):
        ARestaurant.__init__(self, "Concordia")
        self.menu_link = "https://www.menicka.cz/6421-concordia-ristorante-pizzeria.html"
        self.distance = {
            "distance": 0,
            "units": DISTANCE_UNITS.M
        }

    def fetch_menu(self):
        assert self.menu_link != "" and self.menu_link is not None
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for Concordia")
            menu_html = rq.text
            soup_ = bs4.BeautifulSoup(menu_html, "html.parser")
            _, self.distance["distance"], menu_soup = extract_information_menicka(soup_)
            menu = self.parse_menu(menu_soup)
            self.add_menu(menu)

    def parse_menu(self, __menu_html) -> ConcordiaMenu:
        assert __menu_html is not None and __menu_html != ""
        menu = ConcordiaMenu()

        # Parsing soups and drinks
        soups = __menu_html.findAll(class_="polevka")
        for s_ in soups:
            price_soup = s_.find(class_="cena")
            if price_soup is None:
                continue
            price_html = price_soup.text
            # Check if this is a drink (contains volume in liters)
            drink_match = re.search(r"^.*(\d+[\.,]?\d*)\s*L", s_.text, re.IGNORECASE | re.MULTILINE)
            if drink_match:
                drink_name_match = re.match(r"(?P<name>[.\D]*)\s?", drink_match[0])
                assert drink_name_match is not None
                drink_volume_match = re.match(r".*(\d+\,\s\d+)L", drink_match[0], re.IGNORECASE)
                assert drink_volume_match is not None
                volume = float(drink_volume_match.group(1).replace(",", ".").replace(" ", ""))
                price_czk_match = re.match(r"\d+", price_html)
                assert price_czk_match is not None

                menu.add_drink(drink_name_match[0].strip(), volume, int(price_czk_match[0]))
                continue
            else:
                soup_name_match = re.match(r"^(?P<name>[A-ZÁÉĚÍÓÚČĎŘŤŽ\s]+)\s\W", s_.text)
                assert soup_name_match is not None
                soup_item = Soup(soup_name_match.group("name").strip(), 0, MEAL_AMOUNT_UNITS.ML, [])
                price_czk_match = re.match(r"\d+", price_soup)
                if price_czk_match is not None:
                    soup_item.set_price(int(price_czk_match[0]))
                soup_description_match = re.match(r"^(?P<name>[A-ZÁĚÉÍÓÚČĎŘŤŽ\s]+)\s\W\s(?P<description>[a-záéíóýúčďňřěťžš\s\,\.]+)", s_.text, re.MULTILINE)
                if soup_description_match is not None:
                    soup_item.set_detailed_description(soup_description_match.group("description").strip())
                menu.add_soup(soup_item)
                continue

        # Parsing main meals
        main_meals = __menu_html.findAll(class_="jidlo")
        for mm_ in main_meals:
            price_soup = mm_.find(class_="cena").text
            main_meal_name_match = re.search(r"(?P<name>[A-ZÁÉĚÍÓÚČĎŘŤŽ\s]+)\s\W.*", mm_.text)
            assert main_meal_name_match is not None
            main_meal_item = MainMeal(main_meal_name_match.group("name").strip(), 0, MEAL_AMOUNT_UNITS.ML, [])
            price_czk_match = re.match(r"\d+", price_soup)
            if price_czk_match is not None:
                main_meal_item.set_price(int(price_czk_match[0]))
            main_meal_description_match = re.search(r"\W\s(?P<description>[a-záéíóúčďňřěťžýš\s\,\.]+)", mm_.text, re.MULTILINE)
            if main_meal_description_match is not None:
                main_meal_item.set_detailed_description(main_meal_description_match.group("description").strip())
            menu.add_mainmeal(main_meal_item)

        return menu
