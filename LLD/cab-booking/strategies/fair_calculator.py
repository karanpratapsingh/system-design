import abc
import math

from models.cab import CabType, Location


class FairCalculationStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate(
        self, pickup: Location, destination: Location, cab_type: CabType
    ) -> float:
        pass


class SimplePricing(FairCalculationStrategy):
    RATE_PER_KM = 2

    def calculate(
        self, pickup: Location, destination: Location, cab_type: CabType
    ) -> float:
        dist = self.calc_point_distance(pickup, destination)
        price = dist * self.RATE_PER_KM
        return price

    def calc_point_distance(self, p1: Location, p2: Location) -> float:
        dist = math.sqrt(pow(p1.lat - p2.lat, 2) + pow(p1.lng - p2.lng, 2))
        return dist
