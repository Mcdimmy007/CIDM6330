from typing import Dict
from datetime import datetime
from abc import ABC, abstractmethod

"""When a user calls get_forecast, Forecast creates a GetWeatherForecastCommand"""
"""instance with the IWeatherService instance and location."""

class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class GetWeatherForecastCommand(ICommand):
    def __init__(self, weather_service: IWeatherService, location: str) -> None:
        self.weather_service = weather_service
        self.location = location
        self.forecast = None
    
    def execute(self) -> None:
        self.forecast = self.weather_service.get_forecast(self.location)

class IQuery(ABC):
    @abstractmethod
    def execute(self) -> Dict:
        pass

class GetWeatherForecastQuery(IQuery):
    def __init__(self, weather_service: IWeatherService, location: str) -> None:
        self.weather_service = weather_service
        self.location = location
        self.forecast = None
    
    def execute(self) -> Dict:
        return self.weather_service.get_forecast(self.location)

class IWeatherService(ABC):
    @abstractmethod
    def get_forecast(self, location: str) -> Dict:
        pass

class OpenWeatherService(IWeatherService):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    
    def get_forecast(self, location: str) -> Dict:
        # Implementation omitted for brevity
        pass

class WeatherForecast:
    def __init__(self, temperature: float, conditions: str, timestamp: datetime) -> None:
        self.temperature = temperature
        self.conditions = conditions
        self.timestamp = timestamp
    
    def __repr__(self) -> str:
        return f"WeatherForecast(temperature={self.temperature}, conditions='{self.conditions}', timestamp='{self.timestamp}')"

class Forecast:
    def __init__(self, weather_service: IWeatherService) -> None:
        self.weather_service = weather_service
    
    def get_forecast(self, location: str) -> WeatherForecast:
        command = GetWeatherForecastCommand(self.weather_service, location)
        command.execute()
        forecast_data = command.forecast
        
        temperature = forecast_data.get("temperature")
        conditions = forecast_data.get("conditions")
        timestamp_str = forecast_data.get("timestamp")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        
        return WeatherForecast(temperature, conditions, timestamp)

