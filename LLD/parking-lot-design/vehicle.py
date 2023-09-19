import math

from datetime import datetime
from abc import ABC, abstractmethod

from enums import VehicleType, ParkingTicketStatus, ParkingSpotType
import config


class Vehicle(ABC):
    """Vehicle parent abstract class."""

    def __init__(self, vehicle_number, vehicle_type, parking_spot_type, ticket=None):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.ticket = ticket
        self.parking_spot_type = parking_spot_type
        self.parking_time = datetime.utcnow()
        self.ticket_status = ParkingTicketStatus.ACTIVE
        self.exit_time = None
        self.parking_cost = None

    def assign_ticket(self, ticket):
        self.ticket = ticket

    def get_type(self):
        return self.vehicle_type

    def update_parking_status(self, parking_charge):
        self.exit_time = datetime.utcnow()
        self.parking_cost = parking_charge
        self.ticket_status = ParkingTicketStatus.PAID

    @abstractmethod
    def parking_charge(self):
        pass


class Car(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.CAR, ParkingSpotType.COMPACT, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hour = math.ceil((now - self.parking_time).total_seconds() / (60 * 60))
        if parking_hour <= 2:
            return config.CAR_PARKING_RATE[parking_hour]
        return config.CAR_PARKING_RATE[3] * parking_hour


class Van(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.VAN, ParkingSpotType.LARGE, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hour = math.ceil((now - self.parking_time).total_seconds() / (60 * 60))
        if parking_hour <= 2:
            return config.VAN_PARKING_RATE[parking_hour]
        return config.VAN_PARKING_RATE[3] * parking_hour


class Truck(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.TRUCK, ParkingSpotType.LARGE, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hour = math.ceil((now - self.parking_time).total_seconds() / (60 * 60))
        if parking_hour <= 2:
            return config.VAN_PARKING_RATE[parking_hour]
        return config.VAN_PARKING_RATE[3] * parking_hour


class Motorcycle(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.MOTORBIKE, ParkingSpotType.MOTORBIKE, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hour = math.ceil((now - self.parking_time).total_seconds() / (60 * 60))
        if parking_hour <= 2:
            return config.MOTORBIKE_PARKING_RATE[parking_hour]
        return config.MOTORBIKE_PARKING_RATE[3] * parking_hour
