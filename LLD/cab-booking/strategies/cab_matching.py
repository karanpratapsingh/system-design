import abc
import math

from exceptions import NoCabAvailable
from models.cab import Cab, Location


class CabMatchingStrategy(abc.ABC):
    @abc.abstractmethod
    def match(self, pickup: Location, available_cabs: list[Cab]) -> Cab:
        pass


class MatchNearestCab(CabMatchingStrategy):
    def match(self, pickup: Location, available_cabs: list[Cab]) -> Cab:
        available_cabs.sort(key=lambda x: self.shortest_distance(pickup, x.location))
        if len(available_cabs) == 0:
            raise NoCabAvailable("no cabs available for the given type")
        return available_cabs[0]

    def shortest_distance(self, p1: Location, p2: Location) -> float:
        dist = math.sqrt(pow(p1.lat - p2.lat, 2) + pow(p1.lng - p2.lng, 2))
        return dist
