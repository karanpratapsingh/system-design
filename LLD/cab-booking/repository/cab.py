from exceptions import AlreadyExists, DoesNotExists
from models.cab import Cab, CabType


class CabRepo:
    def __init__(self) -> None:
        self.cabs = {}

    def register_cab(self, cab) -> Cab:
        if self.cabs.get(cab.id):
            raise AlreadyExists("cab already exists")
        cab.id = cab.registration_number
        self.cabs[cab.id] = cab

    def update_availability(self, cab_id: str, available: bool):
        if not self.cabs.get(cab_id):
            raise DoesNotExists("cab does not exists")
        self.cabs[cab_id].is_available = available

    def list_available(self, cab_type: CabType) -> list[Cab]:
        return [
            self.cabs[cab_id]
            for cab_id in self.cabs
            if self.cabs[cab_id].is_available and self.cabs[cab_id].cab_type == cab_type
        ]
