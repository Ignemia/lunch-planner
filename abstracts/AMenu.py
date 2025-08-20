import abc
import typing

from ARestaurant import ARestaurant
from AMeal import AMeal

class AMenu:
    def __init__(self):
        self.restaurant = None
        self.meals = {
            "soups": set(),
            "main_meals": set()
        }
        self.drinks = set()

    @abc.abstractmethod
    def add_restaurant(self, restaurant: ARestaurant) -> bool:
        raise NotImplementedError("add_restaurant method has to be implemented")

    def get_restaurant(self) -> typing.Optional[ARestaurant]:
        return self.restaurant

    @abc.abstractmethod
    def add_drink(self, name: str, volume: float) -> bool:
        raise NotImplementedError("add_drink method has to be implemented")

    @abc.abstractmethod
    def add_soup(self, soup: AMeal) -> bool:
        raise NotImplementedError("add_soup method has to be implemented")

    @abc.abstractmethod
    def add_mainmeal(self, meal: AMeal) -> bool:
        raise NotImplementedError("add_mainmeal method has to be implemented")
