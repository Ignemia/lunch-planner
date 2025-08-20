import enum
import typing

class MEAL_AMOUNT_UNITS(enum.StrEnum):
    NONE = ""
    L = "liters"
    ML = "milli liters"
    KG = "kilograms"
    G = "grams"

ALLERGENS_EN = ["Wheats", "Crustatians", "Eggs", "Fish", "Almonds", "Soy", "Milk", "Nuts", "Cillantro", "Mustard", "Sesame", "Sulfur Oxide", "Wolf Bean", "Mollusks"]

class AMeal:
    def __init__(self):
        self.name = None
        self.allergens = dict.fromkeys(range(14), False)
        self.amount = {
            "amount": 0.0,
            "units": MEAL_AMOUNT_UNITS.NONE
        }

    def set_name(self, name: str):
        self.name = name

    def set_allergens(self, allergens: typing.List[int]):
        for index in range(14):
            if index + 1 not in allergens:
                continue
            self.allergens[index] = True

    def set_amount(self, amount: float, unit: MEAL_AMOUNT_UNITS):
        self.amount["amount"] = amount
        self.amount["units"] = unit
