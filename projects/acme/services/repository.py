from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.weather.station import Station, StationHelper


# Create engine and session
engine = create_engine("sqlite:///weather.db")
Session = sessionmaker(bind=engine)

class StationRepository:
    def __init__(self):
        self.session = Session()

    def add(self, station: Station):
        self.session.add(station)
        self.session.commit()

    def add_all(self, stations: List[Station]):
        self.session.add_all(stations)
        self.session.commit()

    def get_by_id(self, station_id: str) -> Station:
        return self.session.query(Station).filter_by(station_id=station_id).first()

    def get_all(self) -> List[Station]:
        return self.session.query(Station).all()

    def delete(self, station: Station):
        self.session.delete(station)
        self.session.commit()

    def delete_by_id(self, station_id: str):
        station = self.get_by_id(station_id)
        if station is not None:
            self.delete(station)