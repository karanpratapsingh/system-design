from enum import Enum


class VehicleType(Enum):
    CAR, TRUCK, VAN, MOTORBIKE = 1, 2, 3, 4


class ParkingSpotType(Enum):
    COMPACT, LARGE, MOTORBIKE = 1, 2, 3


class ParkingTicketStatus(Enum):
    ACTIVE, PAID, LOST = 1, 2, 3
