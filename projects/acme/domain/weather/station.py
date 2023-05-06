"""Two new classes StationQuery and StationQueryHandler are created here"""
from abc import ABC, abstractmethod, abstractproperty

class StationQuery:
    def __init__(self, station_id: str = "", latitude: float = 0.0, longitude: float = 0.0):
        self.station_id = station_id
        self.latitude = latitude
        self.longitude = longitude

class StationQueryHandler:
    def __init__(self, station_helper: StationHelper):
        self.station_helper = station_helper

    def handle(self, query: StationQuery) -> Station:
        if query.station_id:
            return self.station_helper.get_station_from_station_id(query.station_id)
        elif query.latitude and query.longitude:
            return self.station_helper.get_station_from_lat_lon(query.latitude, query.longitude)
        else:
            raise ValueError("Invalid query. You must provide either a station ID or a latitude and longitude.")

class StationHelper(ABC):
    @abstractmethod
    def get_station_from_station_id(self, station_id: str) -> Station:
        pass

    @abstractmethod
    def get_station_from_lat_lon(self, latitude: float, longitude: float) -> Station:
        pass

class NOAAADDSStationHelper(StationHelper):
    def __init__(self, noaa_adds_url: str, noaa_adds_format: str):
        self.noaa_adds_url = noaa_adds_url
        self.noaa_adds_format = noaa_adds_format

    def get_station_from_station_id(self, station_id: str) -> Station:
        xml = self._request_noaa_xml(station_id)
        tree_root = self._parse_noaa_xml(xml)
        station = self._create_station_from_xml_element(tree_root)

        return station

    def get_station_from_lat_lon(self, latitude: float, longitude: float) -> Station:
        pass

    def _create_noaa_request_uri(self, station_id: str) -> str:
        pass

    def _request_noaa_xml(self, station_id: str) -> str:
        # prepare url
        url = self.noaa_adds_url
        format = self.noaa_adds_format

        stations_params = {
            "dataSource": "stations",
            "requestType": "retrieve",
            "format": format,
            "stationString": station_id.strip(),
        }

        # start an empty return value
        response_xml = ""

        try:
            noaa_response = requests.get(url, stations_params)
        except ConnectionError:
            response_xml = ""
        except HTTPError:
            response_xml = ""

        if noaa_response.status_code == 200:
            response_xml = noaa_response.text

        return response_xml

    def _parse_noaa_xml(self, xml: str) -> Element:
        try:
            xml_tree_root = fromstring(xml)
        except ParseError:
            xml_tree_root = None

        return xml_tree_root


def main():
    noaa_adds_url
