import abc
import typing
import enum

from . import AMenu

class DISTANCE_UNITS(enum.Enum):
    M = "meters"
    KM = "kilometers"
    MI = "Miles"
    YARDS = "Yards"

class ARestaurant:
    def __init__(self, name):
        self.name = name
        self.distance = {
            "distance": 0,
            "units": DISTANCE_UNITS.M
        }
        self.menu = None
        self.menu_link = ""

    @abc.abstractmethod
    def set_distance(self, distance: float, units: DISTANCE_UNITS):
        raise NotImplementedError("set_distance has to be implemented!")

    @abc.abstractmethod
    def fetch_menu(self):
        raise NotImplementedError("fetch_menu has to be implemented!")

    def add_menu(self, menu: AMenu):
        self.menu = menu

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance["distance"]

    def get_menu_string(self):
        return str(self.menu)
