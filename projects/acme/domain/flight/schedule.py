from typing import List
from datetime import datetime
from dataclasses import dataclass
from dependency_injector import containers, providers


class Schedule:
    def __init__(self, flight_repository):
        self.flight_repository = flight_repository

    def get_flight_schedule(self, flight_number: str) -> List[datetime]:
        flight = self.flight_repository.get_by_flight_number(flight_number)
        return flight.schedule


@dataclass
class Flight:
    flight_number: str
    schedule: List[datetime]


class FlightRepository:
    def __init__(self):
        self.flights = {}

    def add(self, flight: Flight):
        self.flights[flight.flight_number] = flight

    def get_by_flight_number(self, flight_number: str) -> Flight:
        return self.flights.get(flight_number)


class FlightRepositoryProvider(providers.Singleton):
    def __init__(self):
        super().__init__()

    def _create_instance(self, schedule_config):
        flight_repo = FlightRepository()
        for flight in schedule_config.flights:
            flight_repo.add(flight)
        return flight_repo


class ScheduleContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    flight_repository = FlightRepositoryProvider()

    schedule = providers.Factory(Schedule, flight_repository=flight_repository)


def bootstrap() -> ScheduleContainer:
    schedule_config = ScheduleConfig(
        flights=[
            Flight(flight_number='AA101', schedule=[
                datetime(2023, 5, 10, 8, 30),
                datetime(2023, 5, 10, 12, 0),
                datetime(2023, 5, 10, 16, 30),
            ]),
            Flight(flight_number='AA202', schedule=[
                datetime(2023, 5, 11, 10, 30),
                datetime(2023, 5, 11, 14, 0),
                datetime(2023, 5, 11, 18, 30),
            ]),
            Flight(flight_number='AA303', schedule=[
                datetime(2023, 5, 12, 9, 0),
                datetime(2023, 5, 12, 13, 0),
                datetime(2023, 5, 12, 17, 0),
            ]),
        ]
    )

    schedule_container = ScheduleContainer()
    schedule_container.config.from_object(schedule_config)

    return schedule_container


class ScheduleConfig:
    def __init__(self, flights: List[Flight]):
        self.flights = flights
