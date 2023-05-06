from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

# Domain Model
class Flight:
    def __init__(self, id: int, flight_number: str, departure: str, arrival: str, departure_time: datetime, arrival_time: datetime):
        self.id = id
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time

class FlightRepository(ABC):
    @abstractmethod
    def get_flight_by_id(self, flight_id: int) -> Flight:
        pass

    @abstractmethod
    def get_all_flights(self) -> List[Flight]:
        pass

class InMemoryFlightRepository(FlightRepository):
    def __init__(self):
        self.flights = []

    def get_flight_by_id(self, flight_id: int) -> Flight:
        for flight in self.flights:
            if flight.id == flight_id:
                return flight

    def get_all_flights(self) -> List[Flight]:
        return self.flights

    def add_flight(self, flight: Flight):
        self.flights.append(flight)

class GetFlightByIdQuery:
    def __init__(self, flight_id: int):
        self.flight_id = flight_id

class GetAllFlightsQuery:
    pass

class FlightQueryHandler:
    def __init__(self, flight_repository: FlightRepository):
        self.flight_repository = flight_repository

    def handle(self, query):
        if isinstance(query, GetFlightByIdQuery):
            return self.flight_repository.get_flight_by_id(query.flight_id)
        elif isinstance(query, GetAllFlightsQuery):
            return self.flight_repository.get_all_flights()

class AddFlightCommand:
    def __init__(self, flight: Flight):
        self.flight = flight

class FlightCommandHandler:
    def __init__(self, flight_repository: FlightRepository):
        self.flight_repository = flight_repository

    def handle(self, command):
        if isinstance(command, AddFlightCommand):
            self.flight_repository.add_flight(command.flight)

# Dependency Injection Bootstrapping
flight_repository = InMemoryFlightRepository()
flight_query_handler = FlightQueryHandler(flight_repository)
flight_command_handler = FlightCommandHandler(flight_repository)
