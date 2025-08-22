import requests
import bs4
import re

from menicka_handler import extract_information_menicka
from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS
from models import MainMeal, Soup

class BruxxMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = Bruxx

    def add_soup(self, soup: AMeal) -> bool:
        try:
            self.meals["soups"].add(soup)
            return True
        except:
            return False

class Bruxx(ARestaurant):
    def __init__(self):
        ARestaurant.__init__(self, "Bruxx")
        self.menu_link = "https://www.menicka.cz/2153-bruxx.html"

    def fetch_menu(self):
        assert self.menu_link != "" and self.menu_link is not None
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for Bruxx")
            menu_html = rq.text
            _, self.distance, menu_text = extract_information_menicka(bs4.BeautifulSoup(menu_html, "html.parser"))
            menu = self.parse_menu(menu_text)
            self.add_menu(menu)

    def parse_menu(self, __menu_text) -> BruxxMenu:
        assert __menu_text is not None and __menu_text != ""
        menu = BruxxMenu()
        menicko_soup = bs4.BeautifulSoup(__menu_text, "html.parser")
        soups = menicko_soup.findAll(class_="polevka")
        for s_ in soups:
            allergen_badges = s_.findAll("em")
            price_soup = s_.find(class_="cena")
            match = re.search(r"(?P<soup_name>.*)\s?(?P<amount>\d+[\,\.\s_]+?\d+)\s?(?P<units>m?l)", s_.text)
            if match is None:
                continue
            name = match.group("soup_name").strip()
            volume = int(re.sub(r"\s_", "", match.group("amount").strip()))
            units = match.group("units").strip()
            allergens = [int(al.text) for al in allergen_badges]
            if units != 'ml':
                volume *= 1000
            soup_item = Soup(name, volume, MEAL_AMOUNT_UNITS.ML, allergens)
            soup_item.set_price(int(price_soup))
            menu.add_soup(soup_item)

        main_meals = menicko_soup.findAll(class_="jidlo")
        for mm_ in main_meals:
            allergen_badges = mm_.findAll("em")
            allergens = [int(al.text) for al in allergen_badges]
            price_soup = mm_.find(class_="cena")
            match = re.search(r"(?P<meal_name>.*)\s(?P<amount>\d+)(?P<units>k?g)", mm_.text)
            if match is None:
                continue

            amount = float(match.group("amount"))
            if match.group("units") != 'g':
                amount *= 1000
            mm = MainMeal(match.group("meal_name"), amount, MEAL_AMOUNT_UNITS.G, allergens)
            mm.set_price(int(price_soup.text))
            menu.add_mainmeal(mm)
        return menu
