import requests
import bs4
import re

from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS, DISTANCE_UNITS
from models import MainMeal, Soup

class MlsnejKocourMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = MlsnejKocour
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

class MlsnejKocour(ARestaurant):
    def __init__(self):
        ARestaurant.__init__(self, "MlsnejKocour")
        self.menu_link = "https://www.mlsnejkocour.cz/"  # adjust if you have a direct menu URL
        self.distance = {
            "distance": 0,
            "units": DISTANCE_UNITS.M
        }

    def fetch_menu(self):
        assert self.menu_link != "" and self.menu_link is not None
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for Mlsnej Kocour")
            menu_html = rq.text
            soup_ = bs4.BeautifulSoup(menu_html, "html.parser")
            table = soup_.find("table", class_="dailyMenuTable")
            if table is None:
                print("Menu table not found for Mlsnej Kocour")
                return
            menu = self.parse_menu(table)
            self.add_menu(menu)

    def parse_menu(self, __menu_html) -> MlsnejKocourMenu:
        assert __menu_html is not None and __menu_html != ""
        menu = MlsnejKocourMenu()

        # current_section will be one of: "polévka", "hlavní jídlo", "menu", "malý denní salátek",
        # "vegetariánské jídlo", "dezert", "minutka", "speciality dne", etc.
        current_section = None

        rows = __menu_html.find_all("tr")
        for tr in rows:
            # detect header rows with <h2> inside (section title)
            h2 = tr.find("h2")
            if h2:
                current_section = h2.get_text(separator=" ", strip=True).lower()
                continue

            # non-header rows: usually 3 columns: amount, description, price
            tds = tr.find_all("td")
            if len(tds) < 3:
                continue

            amount_text = tds[0].get_text(separator=" ", strip=True)
            desc_td = tds[1]
            price_text = tds[2].get_text(separator=" ", strip=True)

            # name extraction (join <br> with spaces) then strip
            name_tag = desc_td.find(class_="td-jidlo-obsah")
            if name_tag:
                raw_name = name_tag.get_text(separator=" ", strip=True).strip()
            else:
                raw_name = desc_td.get_text(separator=" ", strip=True).strip()

            # If name contains a hyphen, split into (title, detailed_description).
            # Accept common hyphen/dash characters: -, —, –
            parts = re.split(r'\s*[-—–]\s*', raw_name, maxsplit=1)
            if len(parts) == 2:
                dish_name = parts[0].strip()
                hyphen_description = parts[1].strip()
            else:
                dish_name = raw_name.strip()
                hyphen_description = None

            # normalize price (extract first integer)
            price_match = re.search(r"(\d+)", price_text)
            if price_match:
                price_czk = int(price_match.group(1))
            else:
                # no price found — skip this dish
                continue

            # parse amount and units
            amount_val = 0
            amount_units = None
            if amount_text:
                g_match = re.search(r"(\d+)\s*g", amount_text, flags=re.I)
                ml_match = re.search(r"(\d+)\s*ml", amount_text, flags=re.I)
                l_match = re.search(r"(\d+)\s*l", amount_text, flags=re.I)
                if g_match:
                    amount_val = int(g_match.group(1))
                    amount_units = MEAL_AMOUNT_UNITS.G
                elif ml_match:
                    amount_val = int(ml_match.group(1))
                    amount_units = MEAL_AMOUNT_UNITS.ML
                elif l_match:
                    amount_val = int(l_match.group(1)) * 1000
                    amount_units = MEAL_AMOUNT_UNITS.ML
                else:
                    # fallback: try any leading number
                    any_num = re.match(r"(\d+)", amount_text)
                    if any_num:
                        amount_val = int(any_num.group(1))
                        # if number present but no unit, assume grams for main meals, ml for soups
                        amount_units = MEAL_AMOUNT_UNITS.G

            # decide which model to create based on section
            section = (current_section or "").strip()
            is_soup = "polév" in section  # matches polévka / polévky
            # default units if not parsed
            if amount_units is None:
                amount_units = MEAL_AMOUNT_UNITS.ML if is_soup else MEAL_AMOUNT_UNITS.G

            try:
                if is_soup:
                    soup_item = Soup(dish_name, amount_val, amount_units, [])
                    soup_item.set_price(price_czk)
                    if hyphen_description:
                        soup_item.set_detailed_description(hyphen_description)
                    menu.add_soup(soup_item)
                else:
                    mm = MainMeal(dish_name, amount_val, amount_units, [])
                    mm.set_price(price_czk)
                    if hyphen_description:
                        mm.set_detailed_description(hyphen_description)
                    menu.add_mainmeal(mm)
            except Exception as e:
                # keep parsing even if one item fails
                print(f"Failed to add item '{dish_name}': {e}")
                continue

        return menu
