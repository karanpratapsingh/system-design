from enum import Enum

from models.user import User


class CabType(str, Enum):
    MINI = "mini"
    XL = "xl"
    BLACK = "black"


class Location:
    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng


class Cab:
    def __init__(
        self, driver: User, reg_number: str, location: Location, cab_type: CabType
    ) -> None:
        self.id = None
        self.driver = driver
        self.registration_number = reg_number
        self.location = location
        self.is_available = True
        self.cab_type = cab_type
