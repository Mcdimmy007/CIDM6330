import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.weather.station import Station, StationType

from domain.services.repository import StationRepository

# Create engine and session
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture
def station_repo():
    repo = StationRepository()
    yield repo
    repo.session.close()

def test_station_repository_add(station_repo):
    station = StationHelper.from_dict(
        {
            "station_id": "test",
            "wmo_id": "test",
            "latitude": 10.0,
            "longitude": 20.0,
            "elevation_m": 5.0,
            "site": "Test Station",
            "state": "ST",
            "country": "US",
            "site_type": [StationType.AIRPORT],
        }
    )
    station_repo.add(station)
    assert station_repo.get_by_id("test") == station

def test_station_repository_add_all(station_repo):
    stations = [
        StationHelper.from_dict(
            {
                "station_id": f"test_{i}",
                "wmo_id": f"test_{i}",
                "latitude": 10.0 + i,
                "longitude": 20.0 + i,
                "elevation_m": 5.0 + i,
                "site": f"Test Station {i}",
                "state": "ST",
                "country": "US",
                "site_type": [StationType.AIRPORT],
            }
        )
        for i in range(3)
    ]
    station_repo.add_all(stations)
    assert len(station_repo.get_all()) == 3

def test_station_repository_get_by_id(station_repo):
    station = StationHelper.from_dict(
        {
            "station_id": "test",
            "wmo_id": "test",
            "latitude": 10.0,
            "longitude": 20.0,
            "elevation_m": 5.0,
            "site": "Test Station",
            "state": "ST",
            "country": "US",
            "site_type": [StationType.AIRPORT],
        }
    )
    station_repo.add(station)
    assert station_repo.get_by_id("test") == station

def test_station_repository_get_all(station_repo):
    stations = [
        StationHelper.from_dict(
            {
                "station_id": f"test_{i}",
                "wmo_id": f"test_{i}",
                "latitude": 10.0 + i,
                "longitude": 20.0 + i,
                "elevation_m": 5.0 + i,
                "site": f"Test Station {i}",
                "state": "ST",
                "country": "US",
                "site_type": [StationType.AIRPORT],
            }
        )
        for i in range(3)
    ]
    station_repo.add_all(stations)
    assert station_repo.get_all() == stations

def test_station_repository_delete(station_repo):
    station = StationHelper.from_dict(
        {
            "station_id": "test",
            "wmo_id": "test",
            "latitude": 10.0,
            "longitude": 20.0,
            "elevation_m": 5.0,
            "site": "Test Station",
            "state": "ST",
            "country": "US",
            "site_type": [StationType.AIRPORT],
        }
    )
    station_repo.add(station)
    station_repo.delete(station)
    assert station_repo.get_by_id("test") is None

def test_station_repository_delete
