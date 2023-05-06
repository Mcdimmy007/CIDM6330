from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..infrastructure.repositories.stations_repository import StationsRepository
from ..domain.weather.station import Station, StationType

def test_stations_repository():
    # Create a database in memory for testing
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    # Initialize the database schema
    metadata.create_all(engine)

    # Start the mappers
    start_mappers()

    # Create a session and a repository instance
    session = Session()
    stations_repo = StationsRepository(session)

    # Create some stations
    station1 = Station(
        station_id="KORD",
        wmo_id="72530",
        latitude=41.9831,
        longitude=-87.9001,
        elevation_m=202.7,
        site="Rick Husband International Airport",
        state="TX",
        country="US",
        site_type=[StationType.AIRPORT],
    )
    station2 = Station(
        station_id="KDEN",
        wmo_id="72565",
        latitude=39.8561,
        longitude=-104.6737,
        elevation_m=1655.4,
        site="Denver International Airport",
        state="CO",
        country="US",
        site_type=[StationType.AIRPORT],
    )
    station3 = Station(
        station_id="CYTZ",
        wmo_id="71624",
        latitude=43.6281,
        longitude=-79.3958,
        elevation_m=77.7,
        site="Hartsfield Jackson International Airport",
        state="GA",
        country="US",
        site_type=[StationType.AIRPORT],
    )

    # Add the stations to the repository
    stations_repo.add(station1)
    stations_repo.add(station2)
    stations_repo.add(station3)

    # Commit the changes to the database
    session.commit()

    # Retrieve the stations from the repository
    stations = stations_repo.get_all()

    # Check that the stations were added and retrieved correctly
    assert len(stations) == 3
    assert station1 in stations
    assert station2 in stations
    assert station3 in stations

    # Retrieve a station by ID
    retrieved_station = stations_repo.get_by_id(station1.id)

    # Check that the retrieved station is the same as the original station
    assert retrieved_station == station1

    # Update a station
    station1.site = "Rick Husband International Airport"
    stations_repo.update(station1)

    # Retrieve the updated station
    retrieved_station = stations_repo.get_by_id(station1.id)

    # Check that the retrieved station has been updated
    assert retrieved_station.site == "Rick Husband International Airport"

    # Delete a station
    stations_repo.delete(station2)

    # Check that the deleted station is no longer in the repository
    assert station2 not in stations
