import abc
import typing
import enum
from typing_extensions import ClassVar, Dict

from . import AMenu

class DISTANCE_UNITS(enum.Enum):
    M = "meters"
    KM = "kilometers"
    MI = "Miles"
    YARDS = "Yards"

class ARestaurant:
    Instances: ClassVar[Dict] = {}

    def __init__(self, name):
        self.name = name
        self.distance = {
            "distance": 0,
            "units": DISTANCE_UNITS.M
        }
        self.menu = None
        self.menu_link = ""
        if name not in ARestaurant.Instances:
             ARestaurant.Instances[name] = self

    @staticmethod
    def get_instance(impl, name: str):
        if name not in ARestaurant.Instances:
            impl()
        return ARestaurant.Instances[name]

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

    def get_menu(self):
        return self.menu
