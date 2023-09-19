import json
import time

from enums import VehicleType

import config


class ParkingLot:
    """ParkingLot system."""

    def __init__(self, name):
        self.name = name
        self.compact_spot_count = 0
        self.large_spot_count = 0
        self.motorbike_spot_count = 0
        self.max_compact_count = config.COMPACT_COUNT
        self.max_large_count = config.LARGE_COUNT
        self.max_motorbike_count = config.MOTORBIKE_COUNT

        # all active parking tickets, identified by their ticket_number
        self.active_tickets = {}
        self.parking_history = {}

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_new_parking_ticket(self, vehicle):
        """Park vehicle in parking lot if spot is available.
        Args: vehicle object

        Returns: ticket number
        """
        if self.is_full(vehicle.get_type()):
            return 'Parking full!'

        ticket = int(time.time() * 100)  # Generate unique tickets  number
        vehicle.assign_ticket(ticket)
        self._increment_spot_count(vehicle.get_type())
        self.active_tickets[ticket] = vehicle
        self.parking_history[ticket] = vehicle
        return ticket

    def is_full(self, vehicle_type):
        """Check parking lot status.

        Args: string vehicle_type

        Returns: boolean value
        """
        # trucks and vans can only be parked in LargeSpot
        if vehicle_type == VehicleType.TRUCK or vehicle_type == VehicleType.VAN:
            return self.large_spot_count >= self.max_large_count

        # motorbikes can only be parked at motorbike spots
        if vehicle_type == VehicleType.MOTORBIKE:
            return self.motorbike_spot_count >= self.max_motorbike_count

        # cars can be parked at compact or large spots
        if vehicle_type == VehicleType.CAR:
            return (self.compact_spot_count + self.large_spot_count) >= (
                    self.max_compact_count + self.max_large_count)

    def _increment_spot_count(self, vehicle_type):
        """Update parking spot count.

        Args: string vehicle_type

        Returns None
        """
        if vehicle_type == VehicleType.TRUCK or vehicle_type == VehicleType.VAN:
            self.large_spot_count += 1
        elif vehicle_type == VehicleType.MOTORBIKE:
            self.motorbike_spot_count += 1
        elif vehicle_type == VehicleType.CAR:
            if self.compact_spot_count < self.max_compact_count:
                self.compact_spot_count += 1
            else:
                self.large_spot_count += 1

    def _decrement_spot_count(self, vehicle_type):
        """Update parking spot count.

        Args: string vehicle_type

        Returns: None
        """
        if vehicle_type == VehicleType.TRUCK or vehicle_type == VehicleType.VAN:
            self.large_spot_count -= 1
        elif vehicle_type == VehicleType.MOTORBIKE:
            self.motorbike_spot_count -= 1
        elif vehicle_type == VehicleType.CAR:
            self.large_spot_count -= 1

    def leave_parking(self, ticket_number):
        """Exit vehicle from parking. Remove vehicle from active_tickets and calculate parking charges.

        Args:
            ticket_number: int ticket_number

        Returns: vehicle_number and parking_charge
        """
        if ticket_number in self.active_tickets:
            vehicle = self.active_tickets[ticket_number]
            self._decrement_spot_count(vehicle.get_type())
            parking_charge = vehicle.parking_charge()
            vehicle.update_parking_status(parking_charge)
            self.parking_history[ticket_number] = vehicle
            self.active_tickets.pop(vehicle.ticket, None)
            return vehicle.vehicle_number, parking_charge
        return 'Invalid ticket number.', None

    def vehicle_status(self, ticket_number):
        """Check vehicle status.

        Args: int ticket_number

        Returns: string vehicle details
        """
        if ticket_number in self.parking_history:
            vehicle = self.parking_history[ticket_number]
            vehicle_details = {
                "Vehicle Number": vehicle.vehicle_number,
                "Vehicle Type": vehicle.vehicle_type.name,
                "Vehicle parking spot type": vehicle.parking_spot_type.name,
                "Vehicle parking time": vehicle.parking_time.strftime("%d-%m-%Y, %H:%M:%S"),
                "Vehicle parking charges": vehicle.parking_cost,
                "vehicle ticket status": vehicle.ticket_status.name,
            }
            return vehicle_details
        return 'Invalid ticket number.'

    def get_empty_spot_number(self):
        """Return available parking spot.

        Returns: available parking space.
        """
        message = ""
        if self.max_compact_count - self.compact_spot_count > 0:
            message += f"Free Compact: {self.max_compact_count - self.compact_spot_count}"
        else:
            message += "Compact is full"
        message += "\n"

        if self.max_large_count - self.large_spot_count > 0:
            message += f"Free Large: {self.max_large_count - self.large_spot_count}"
        else:
            message += "Large is full"
        message += "\n"

        if self.max_motorbike_count - self.motorbike_spot_count > 0:
            message += f"Free Motorbike: {self.max_motorbike_count - self.motorbike_spot_count}"
        else:
            message += "Motorbike is full"
        message += "\n"

        return message
