from abstracts import AMeal, MEAL_AMOUNT_UNITS

import typing

class MainMeal(AMeal):
    def __init__(self, name: str, amount: float, units: MEAL_AMOUNT_UNITS, allergens: typing.List[int]):
        super().__init__()
        self.set_name(name)
        self.set_amount(amount, units)
        self.set_allergens(allergens)
