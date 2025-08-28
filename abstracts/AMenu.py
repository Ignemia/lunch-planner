import abc
import typing

from .ARestaurant import ARestaurant
from .AMeal import AMeal

class AMenu:
    def __init__(self):
        self.restaurant = None
        self.meals = {
            "soups": set(),
            "main_meals": set()
        }
        self.drinks = set()

    def get_restaurant(self) -> typing.Optional[ARestaurant]:
        return self.restaurant

    @abc.abstractmethod
    def add_drink(self, name: str, volume: float, price_czk: int) -> bool:
        '''
        Adds drink to menu

        @param: [name: <str>] name of the drink as provided on the menu
        @param: [volume: <float>] amount of drink in millilitres
        @param: [price_czk: <float>] Drink price in czech crowns
        @returns: <bool>
            - True:     Drink added successfully
            - False:    Adding drink failed
        '''
        raise NotImplementedError("add_drink method has to be implemented")

    @abc.abstractmethod
    def add_soup(self, soup: AMeal) -> bool:
        '''
        Adds soup to menu

        @param: [name: <str>] name of the soup as provided on the menu
        @param: [volume: <float>] amount of drink in litres
        @returns: <bool>
            - True:     Soup added successfully
            - False:    Adding Soup failed
        '''
        raise NotImplementedError("add_soup method has to be implemented")

    @abc.abstractmethod
    def add_mainmeal(self, meal: AMeal) -> bool:
        '''
        Adds main meal to menu

        @param: [name: <str>] name of the main meal as provided on the menu
        @param: [volume: <float>] amount of main meal in provided amount
        @returns: <bool>
            - True:     Mean meal added successfully
            - False:    Adding main meal failed
        '''
        raise NotImplementedError("add_mainmeal method has to be implemented")

    def __str__(self) -> str:
        out = ""
        if len(self.drinks) > 0:
            out += "Drinks:\n"
            for id, drink in enumerate(self.drinks):
                out += f"\t\t{(id+1)} - {str(drink)}\n"
        if len(self.meals["soups"]) > 0:
            out += "\tSoups:\n"
            for id, soup in enumerate(self.meals["soups"]):
                out += f"\t\t{(id+1)} - {str(soup)}\n"
        out += "\tMain Meals:\n"
        for id, mm in enumerate(self.meals["main_meals"]):
            out += f"\t\t{(id+1)} - {str(mm)}\n"
        return out

    def get_main_meals(self):
        return self.meals["main_meals"]
