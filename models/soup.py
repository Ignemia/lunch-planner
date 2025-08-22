from abstracts import AMeal, MEAL_AMOUNT_UNITS

import typing

class Soup(AMeal):
    def __init__(self, name: str, volume: float, units: MEAL_AMOUNT_UNITS, allergens: typing.List[int]):
        super().__init__()
        self.set_allergens(allergens)
        self.set_name(name)
        self.set_amount(volume, units)
