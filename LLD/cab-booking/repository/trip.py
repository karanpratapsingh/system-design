from exceptions import AlreadyExists, DoesNotExists
from models.trip import Trip


class TripRepo:
    def __init__(self) -> None:
        self.trips = {}

    def create(self, trip: Trip) -> None:
        if trip.id in self.trips:
            raise AlreadyExists("trip already exists")
        trip.id = f"trip_{trip.cab.registration_number}"
        self.trips[trip.id] = trip

    def get(self, trip_id: str) -> Trip:
        if trip_id not in self.trips:
            raise DoesNotExists("trip not found")
        return self.trips[trip_id]

    def update(self, trip):
        if trip.id not in self.trips:
            raise DoesNotExists("trip not found")
        self.trips[trip.id] = trip

    def list_rider_trips(self, user_id) -> list[Trip]:
        trips = [trip for trip in self.trips.values() if trip.rider.id == user_id]
        return trips

    def list_driver_trips(self, driver_id) -> list[Trip]:
        trips = [trip for trip in self.trips.values() if trip.driver.id == driver_id]
        return trips
