import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherReading:
    timestamp: datetime.datetime
    temperature: float  # Celsius
    humidity: float  # Percentage
    wind_direction: float  # 0-360 degrees
    wind_direction_name: str
    wind_force: int  # Beaufort
    wind_speed: float  # m/s
    wind_gust_speed: float  # m/s


class WeatherAPI(ABC):

    @abstractmethod
    def fetch_reading(self) -> Optional[WeatherReading]:
        pass
