import abc
import typing
import enum

from AMenu import AMenu

class DISTANCE_UNITS(enum.StrEnum):
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

    @abc.abstractmethod
    def set_distance(self, distance: float, units: DISTANCE_UNITS):
        raise NotImplementedError("set_distance has to be implemented!")

    @abc.abstractmethod
    def add_menu(self, menu: AMenu):
        raise NotImplementedError("add_menu has to be implemented!")
