import requests
from abstracts.AMeal import MEAL_AMOUNT_UNITS
import bs4
import re

from menicka_handler import extract_information_menicka
from abstracts import AMenu, ARestaurant
from models.soup import Soup

class BruxxMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = Bruxx

    def add_drink(self, name: str, volume: float) -> bool:
        try:
            return True
        except:
            return False
    def add_soup(self, soup: Soup) -> bool:
        try:
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

    def parse_menu(self, __menu_text)
        assert __menu_text is not None and __menu_text != ""
        menu = BruxxMenu()
        menicko_soup = bs4.BeautifulSoup(__menu_text, "html.parser")
        soups = menicko_soup.findAll(class_="polevka")
        for s in soups:
            allergen_badges = s.findAll("em")
            match = re.search(r"(.*)(\d+[\,\.\s]+?\d+)(m?l)", s.text)
            if match is None:
                continue
            name = match.group(1).strip()
            volume = int(re.sub(r"\s", "", match.group(2).strip()))
            units = match.group(3).strip()
            allergens = [int(al.text) for al in allergen_badges]
            if units != 'ml':
                volume *= 1000
            menu.add_soup(Soup(name, volume, MEAL_AMOUNT_UNITS.ML, allergens))
