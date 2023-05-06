from typing import List
from datetime import datetime
from acme.flight import Flight, Reservation
from acme.flight import FlightRepository, ReservationRepository


class SchedulePilotCommand:
    def __init__(self, pilot_id: int, flight_id: int, departure_time: datetime):
        self.pilot_id = pilot_id
        self.flight_id = flight_id
        self.departure_time = departure_time


class SchedulePilotCommandHandler:
    def __init__(self, pilot_repository: PilotRepository, flight_repository: FlightRepository,
                 reservation_repository: ReservationRepository):
        self.pilot_repository = pilot_repository
        self.flight_repository = flight_repository
        self.reservation_repository = reservation_repository

    def execute(self, command: SchedulePilotCommand):
        pilot = self.pilot_repository.get_by_id(command.pilot_id)
        flight = self.flight_repository.get_by_id(command.flight_id)
        reservation = Reservation(pilot=pilot, flight=flight, departure_time=command.departure_time)
        self.reservation_repository.save(reservation)


class PilotScheduleQuery:
    def __init__(self, pilot_id: int):
        self.pilot_id = pilot_id


class PilotScheduleQueryHandler:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def execute(self, query: PilotScheduleQuery) -> List[Reservation]:
        return self.reservation_repository.get_by_pilot_id(query.pilot_id)
