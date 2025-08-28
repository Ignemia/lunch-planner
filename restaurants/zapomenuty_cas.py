import requests
import bs4
import re

from abstracts import AMenu, ARestaurant, AMeal, MEAL_AMOUNT_UNITS, DISTANCE_UNITS
from models import MainMeal, Soup

class ZapomenutyCasMenu(AMenu):
    def __init__(self):
        super().__init__()
        self.restaurant = ZapomenutyCas
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

class ZapomenutyCas(ARestaurant):
    def __init__(self):
        # Name intentionally glued together as requested
        ARestaurant.__init__(self, "ZapomenutyCas")
        self.menu_link = "https://www.zapomenutycas.cz/"
        self.distance = {"distance": 0, "units": DISTANCE_UNITS.M}

    def fetch_menu(self):
        assert self.menu_link
        with requests.get(self.menu_link) as rq:
            if rq.status_code != 200:
                raise Exception("Couldn't fetch menu for ZapomenutyCas")
            menu_html = rq.text
            soup_ = bs4.BeautifulSoup(menu_html, "html.parser")
            # Wix usually wraps the daily menu in a rich-text div; try the known id first, fallback to any rich-text block
            root = soup_.find(id="comp-lr3v9mws") or soup_.find(class_="wixui-rich-text")
            if root is None:
                print("Menu root not found for ZapomenutyCas")
                return
            menu = self.parse_menu(root)
            self.add_menu(menu)

    def parse_menu(self, __menu_html) -> ZapomenutyCasMenu:
        assert __menu_html is not None and __menu_html != ""
        menu = ZapomenutyCasMenu()

        # helper to normalize weird whitespace characters and collapse multiple spaces
        def clean_text(s: str) -> str:
            if not s:
                return ""
            # replace common invisible/odd whitespace with a normal space
            s = re.sub(r'[\u00A0\u200B\u200C\u200D\uFEFF]', ' ', s)
            # collapse any whitespace runs (tabs, newlines, multiple spaces) to single space
            s = re.sub(r'\s+', ' ', s)
            return s.strip()

        current_section = None     # 'soup', 'main', etc.
        pending_lines = []         # accumulate name/desc lines until we hit a meta line (allergens/price)

        p_tags = __menu_html.find_all("p")
        for p in p_tags:
            # get_text with spaces, then normalize
            raw_text = p.get_text(separator=" ", strip=True)
            text = clean_text(raw_text)
            if not text:
                continue
            lower = text.lower()

            # section headers
            if "polévk" in lower or "polévka" in lower:
                current_section = "soup"
                pending_lines = []
                continue
            if "hlavní" in lower:
                current_section = "main"
                pending_lines = []
                continue

            # explicitly ignore bottles/takeaway sections (we do not handle drinks/takeout)
            if "lahve" in lower or "lahve s sebou" in lower:
                current_section = None
                pending_lines = []
                continue

            # detect meta line that contains allergens/weight/price info or explicit "A ###" price
            is_meta = "alergen" in lower or "| cen" in lower or re.search(r"\bA\s*\d{2,4}\b", text) \
                      or re.search(r"\d{2,4}\s*(?:kč|\,-|,-)", text, flags=re.I)

            if is_meta:
                # join pending lines to form the dish title (and possible multi-line description)
                raw_name = " ".join(pending_lines).strip()
                raw_name = clean_text(raw_name)
                pending_lines = []

                # if no section (or no name), skip — this prevents adding drinks/takeaway or stray meta-lines
                if not raw_name or current_section is None:
                    continue

                # hyphen split (if present) -> left = name, right = detailed description
                parts = re.split(r'\s*[-—–]\s*', raw_name, maxsplit=1)
                if len(parts) == 2:
                    dish_name = clean_text(parts[0])
                    hyphen_description = clean_text(parts[1])
                else:
                    dish_name = clean_text(raw_name)
                    hyphen_description = None

                # amount parsing (look for e.g. '200g', '150g', '0,5l' — l will be converted to ml if present)
                amount_val = 0
                amount_units = None
                g_match = re.search(r'(\d+)\s*g', text, flags=re.I)
                ml_match = re.search(r'(\d+)\s*ml', text, flags=re.I)
                l_match = re.search(r'(\d+[,.]\d+)\s*l', text, flags=re.I)
                if g_match:
                    amount_val = int(g_match.group(1))
                    amount_units = MEAL_AMOUNT_UNITS.G
                elif ml_match:
                    amount_val = int(ml_match.group(1))
                    amount_units = MEAL_AMOUNT_UNITS.ML
                elif l_match:
                    liters = float(l_match.group(1).replace(",", "."))
                    amount_val = int(liters * 1000)
                    amount_units = MEAL_AMOUNT_UNITS.ML

                # price parsing: take the last 2-4 digit integer in the meta line as price (works for "A 169", "49,-", "175 Kč")
                int_matches = re.findall(r'(\d{2,4})', text)
                if not int_matches:
                    # nothing to attach as price — skip item
                    continue
                price_czk = int(int_matches[-1])

                try:
                    is_soup = (current_section == "soup")
                    # if no explicit amount found, choose sensible default
                    if amount_units is None:
                        amount_units = MEAL_AMOUNT_UNITS.ML if is_soup else MEAL_AMOUNT_UNITS.G

                    if is_soup:
                        s = Soup(dish_name, amount_val, amount_units, [])
                        s.set_price(price_czk)
                        if hyphen_description:
                            s.set_detailed_description(hyphen_description)
                        menu.add_soup(s)
                    else:
                        mm = MainMeal(dish_name, amount_val, amount_units, [])
                        mm.set_price(price_czk)
                        if hyphen_description:
                            mm.set_detailed_description(hyphen_description)
                        menu.add_mainmeal(mm)
                except Exception as e:
                    print(f"Failed to add parsed item '{dish_name}': {e}")

                continue

            # otherwise treat this p as part of the dish name/description that precedes a meta line
            pending_lines.append(text)

        return menu
