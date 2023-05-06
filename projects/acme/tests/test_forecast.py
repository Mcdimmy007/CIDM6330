import pytest
from datetime import datetime
from unittest.mock import Mock

from forecast import (
    Forecast,
    GetWeatherForecastCommand,
    GetWeatherForecastQuery,
    IWeatherService,
    WeatherForecast,
)


class MockWeatherService(IWeatherService):
    def __init__(self, data: dict):
        self.data = data
    
    def get_forecast(self, location: str):
        return self.data.get(location)


def test_get_forecast_command_execute():
    weather_service_mock = MockWeatherService({"New York": {"temperature": 72.4, "conditions": "Sunny", "timestamp": "2023-05-06 12:00:00"}})
    command = GetWeatherForecastCommand(weather_service_mock, "New York")
    command.execute()
    assert command.forecast == {"temperature": 72.4, "conditions": "Sunny", "timestamp": "2023-05-06 12:00:00"}


def test_get_forecast_query_execute():
    weather_service_mock = MockWeatherService({"New York": {"temperature": 72.4, "conditions": "Sunny", "timestamp": "2023-05-06 12:00:00"}})
    query = GetWeatherForecastQuery(weather_service_mock, "New York")
    result = query.execute()
    assert result == {"temperature": 72.4, "conditions": "Sunny", "timestamp": "2023-05-06 12:00:00"}


def test_get_forecast():
    weather_service_mock = MockWeatherService({"New York": {"temperature": 72.4, "conditions": "Sunny", "timestamp": "2023-05-06 12:00:00"}})
    forecast = Forecast(weather_service_mock)
    result = forecast.get_forecast("New York")
    assert isinstance(result, WeatherForecast)
    assert result.temperature == 72.4
    assert result.conditions == "Sunny"
    assert result.timestamp == datetime(2023, 5, 6, 12, 0, 0)
