from abstracts import AMeal, MEAL_AMOUNT_UNITS


class Drink(AMeal):
    def __init__(self, name: str, volume: float, price_czk: int):
        super().__init__()
        self.name = name
        self.amount = {
            "amount": volume,
            "units": MEAL_AMOUNT_UNITS.L
        }
        self.price = price_czk
