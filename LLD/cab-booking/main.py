from exceptions import AlreadyExists, DoesNotExists, NoCabAvailable
from models.cab import Cab, CabType, Location
from models.user import User
from repository.cab import CabRepo
from repository.trip import TripRepo
from repository.user import UserRepo
from services.trip import TripService
from strategies.cab_matching import MatchNearestCab
from strategies.fair_calculator import SimplePricing


def test_cab_booking():
    cab_repo = CabRepo()
    user_repo = UserRepo()
    trip_repo = TripRepo()

    nearest_cab_matching_strategy = MatchNearestCab()
    simple_fare_calculator = SimplePricing()
    trip_service = TripService(
        cab_repo,
        trip_repo,
        user_repo,
        nearest_cab_matching_strategy,
        simple_fare_calculator,
    )

    driver = user_repo.register_user(
        User(
            name="Driver",
            email="driver@example.com",
        )
    )
    cab = cab_repo.register_cab(
        Cab(
            driver=driver,
            reg_number="KA-01-HH-1234",
            location=Location(lat=12.97, lng=77.59),
            cab_type=CabType.MINI,
        )
    )
    rider = user_repo.register_user(
        User(
            name="Rider",
            email="rider@example.com",
        )
    )

    trip = trip_service.create_trip(
        rider.id,
        pickup=Location(lat=12.99, lng=77.62),
        destination=Location(lat=13.0, lng=77.64),
        cab_type=CabType.MINI,
    )
    trip_service.start_trip(trip)
    trip_service.end_trip(trip.id)

    print(trip_repo.list_rider_trips(rider.id))


if __name__ == "__main__":
    try:
        test_cab_booking()
    except (DoesNotExists, AlreadyExists, NoCabAvailable) as e:
        print(e)
