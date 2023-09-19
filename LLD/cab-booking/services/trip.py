import abc
from datetime import datetime
import time

from models.cab import CabType, Location
from models.trip import Trip
from repository.cab import CabRepo
from repository.trip import TripRepo
from repository.user import UserRepo
from strategies.cab_matching import CabMatchingStrategy
from strategies.fair_calculator import FairCalculationStrategy


class TripService:
    def __init__(
        self,
        cab_repo: CabRepo,
        trip_repo: TripRepo,
        user_repo: UserRepo,
        cab_matching_strategy: CabMatchingStrategy,
        fare_calculator: FairCalculationStrategy,
    ) -> None:
        self.cab_repo = cab_repo
        self.trip_repo = trip_repo
        self.user_repo = user_repo
        self.cab_matching_strategy = cab_matching_strategy
        self.fare_calculator = fare_calculator

    def create_trip(
        self, user_id, pickup: Location, destination: Location, cab_type: CabType
    ) -> Trip:
        available_cabs = self.cab_repo.list_available(cab_type)
        cab = self.cab_matching_strategy.match(pickup, available_cabs)
        estimated_fare = self.fare_calculator.calculate(pickup, destination, cab_type)
        user = self.user_repo.get(user_id)
        self.cab_repo.update_availability(cab.id, False)
        trip = Trip(pickup, destination, cab, user, estimated_fare)
        self.trip_repo.create(trip)
        return trip

    def start_trip(self, trip):
        trip.started_at = datetime.now()
        self.trip_repo.update(trip)

    def end_trip(self, trip_id):
        trip = self.trip_repo.get(trip_id)
        trip.ended_at = datetime.now()
        self.trip_repo.update(trip)
        self.cab_repo.update_availability(trip.cab.id, True)
