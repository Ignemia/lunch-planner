import requests
import bs4
import re

from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS, DISTANCE_UNITS
from models import MainMeal, Soup

class ParlamentMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = Parlament
        self.meals = {"soups": set(), "main_meals": set()}

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

class Parlament(ARestaurant):
    def __init__(self):
        ARestaurant.__init__(self, "Parlament")
        self.menu_link = "https://www.vinohradskyparlament.cz/"
        self.distance = {"distance": 0, "units": DISTANCE_UNITS.M}

    def fetch_menu(self):
        assert self.menu_link
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for Parlament")
            menu_html = rq.text
            soup_ = bs4.BeautifulSoup(menu_html, "html.parser")
            # menu is inside .container -> #daily-menu or .dm-cat blocks
            daily = soup_.find(id="daily-menu") or soup_.find(class_="container")
            if daily is None:
                print("Menu root not found for Parlament")
                return
            menu = self.parse_menu(daily)
            self.add_menu(menu)

    def parse_menu(self, __menu_html) -> ParlamentMenu:
        assert __menu_html is not None and __menu_html != ""
        menu = ParlamentMenu()

        # helper to normalize weird whitespace characters and collapse multiple spaces
        def clean_text(s: str) -> str:
            if not s:
                return ""
            s = re.sub(r'[\u00A0\u200B\u200C\u200D\uFEFF]', ' ', s)
            s = re.sub(r'\s+', ' ', s)
            return s.strip()

        # iterate dm-cat blocks that are visible (skip those with 'hidden' in class)
        dm_cats = __menu_html.find_all("div", class_="dm-cat")
        for cat in dm_cats:
            classes = cat.get("class") or []
            if "hidden" in classes:
                continue

            # try to read header title (h2)
            h2 = cat.find("h2")
            section_title = clean_text(h2.get_text()) if h2 else ""
            section_lower = section_title.lower()

            # classify section: soups vs main (default to main)
            is_soup_section = "polév" in section_lower or "polévky" in section_lower

            # find items inside this category
            items = cat.find_all("div", class_="dm-item")
            for item in items:
                # content block
                content = item.find("div", class_="dm-content")
                if content is None:
                    continue

                # name: h3 text
                h3 = content.find("h3")
                print(h3)
                raw_name = clean_text(h3.get_text()) if h3 else ""
                if not raw_name:
                    continue

                # hyphen splitting -> name and detailed_description
                parts = re.split(r'\s*[-—–]\s*', raw_name, maxsplit=1)
                if len(parts) == 2:
                    dish_name = clean_text(parts[0])
                    hyphen_description = clean_text(parts[1])
                else:
                    dish_name = clean_text(raw_name)
                    hyphen_description = None

                # amount: <span class="mnoz"> then next <span> unit (commonly g / l / ks)
                amount_val = 0
                amount_units = None
                mnoz = content.find("span", class_="mnoz")
                if mnoz:
                    mnoz_text = clean_text(mnoz.get_text())
                    # try to find unit from the sibling span (next span without class or direct text)
                    unit_span = None
                    # look for the next sibling span after mnoz
                    next_sib = mnoz.find_next_sibling("span")
                    if next_sib:
                        unit_span = clean_text(next_sib.get_text())
                    # normalize decimal commas
                    mnoz_text = mnoz_text.replace(",", ".")
                    # interpret
                    try:
                        if unit_span and unit_span.lower().startswith("l"):
                            liters = float(mnoz_text)
                            amount_val = int(liters * 1000)
                            amount_units = MEAL_AMOUNT_UNITS.ML
                        elif unit_span and unit_span.lower().startswith("ks"):
                            # pieces — keep as grams=0 and unit None (or treat as G if you prefer)
                            amount_val = int(float(mnoz_text))
                            amount_units = None
                        else:
                            # treat as grams by default when unit is numeric (150 -> 150 g)
                            amount_val = int(float(mnoz_text))
                            amount_units = MEAL_AMOUNT_UNITS.G
                    except Exception:
                        amount_val = 0
                        amount_units = None

                # description paragraph
                p = content.find("p")
                description = clean_text(p.get_text()) if p else None

                # price: strong.cen text like "169 Kč"
                price_tag = content.find("strong", class_="cen")
                price_czk = None
                if price_tag:
                    price_text = clean_text(price_tag.get_text())
                    m = re.search(r'(\d{2,4})', price_text)
                    if m:
                        price_czk = int(m.group(1))

                # if no price found, skip
                if price_czk is None:
                    continue

                # default units if none parsed
                if amount_units is None:
                    amount_units = MEAL_AMOUNT_UNITS.ML if is_soup_section else MEAL_AMOUNT_UNITS.G

                # create model and attach metadata
                try:
                    if is_soup_section:
                        s = Soup(dish_name, amount_val, amount_units, [])
                        s.set_price(price_czk)
                        if hyphen_description and not description:
                            s.set_detailed_description(hyphen_description)
                        elif description:
                            s.set_detailed_description(description)
                        menu.add_soup(s)
                    else:
                        mm = MainMeal(dish_name, amount_val, amount_units, [])
                        mm.set_price(price_czk)
                        # prefer <p> description; if none, use hyphen description
                        if description:
                            mm.set_detailed_description(description)
                        elif hyphen_description:
                            mm.set_detailed_description(hyphen_description)
                        menu.add_mainmeal(mm)
                except Exception as e:
                    # keep parsing others
                    print(f"Parlament: failed to add item '{dish_name}': {e}")
                    continue

        print(menu)
        return menu
