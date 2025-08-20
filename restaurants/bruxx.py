import requests
import bs4

from abstracts.ARestaurant import ARestaurant


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
            soup = bs4.BeautifulSoup(menu_html)
