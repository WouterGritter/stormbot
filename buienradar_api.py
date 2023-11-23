from typing import Optional

from buienradar.buienradar import get_data, parse_data
from buienradar.constants import SUCCESS, CONTENT, RAINCONTENT, TEMPERATURE, MEASURED, DATA, HUMIDITY, WINDDIRECTION, \
    WINDAZIMUTH, WINDFORCE, WINDSPEED, WINDGUST

from weather_api import WeatherAPI, WeatherReading


class BuienradarWeatherAPI(WeatherAPI):

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def fetch_reading(self) -> Optional[WeatherReading]:
        timeframe = 5

        result = get_data(latitude=self.latitude, longitude=self.longitude)

        if not result.get(SUCCESS):
            return None

        data = result[CONTENT]
        rain_data = result[RAINCONTENT]

        result = parse_data(data, rain_data, self.latitude, self.longitude, timeframe)
        return WeatherReading(
            timestamp=result[DATA][MEASURED],
            temperature=result[DATA][TEMPERATURE],
            humidity=result[DATA][HUMIDITY],
            wind_direction=result[DATA][WINDAZIMUTH],
            wind_direction_name=result[DATA][WINDDIRECTION],
            wind_force=result[DATA][WINDFORCE],
            wind_speed=result[DATA][WINDSPEED],
            wind_gust_speed=result[DATA][WINDGUST],
        )
