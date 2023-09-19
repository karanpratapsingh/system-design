from datetime import datetime
from models.cab import Cab, Location
from models.user import User


class Trip:
    def __init__(
        self,
        from_location: Location,
        destination: Location,
        cab: Cab,
        rider: User,
        estimated_fare: float,
    ) -> None:
        self.from_location = from_location
        self.destination = destination
        self.cab = cab
        self.rider = rider
        self.fare = estimated_fare
        self.requested_at = datetime.now()
        self.started_at: datetime = None
        self.ended_at: datetime = None
        self.id = None

    def __repr__(self) -> str:
        return f"Trip(cab={self.cab.registration_number}, rider={self.rider.id})"
