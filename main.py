import os
import time
from typing import Optional

from discord_webhook import DiscordWebhook

from buienradar_api import BuienradarWeatherAPI
from weather_api import WeatherAPI, WeatherReading

print(f'{os.environ=}')

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
LATITUDE = float(os.environ.get('LATITUDE'))
LONGITUDE = float(os.environ.get('LONGITUDE'))
WIND_FORCE_THRESHOLD = int(os.environ.get('WIND_FORCE_THRESHOLD'))
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL'))

print(f'DISCORD_WEBHOOK_URL={DISCORD_WEBHOOK_URL[:50]}...')
print(f'{LATITUDE=}')
print(f'{LONGITUDE=}')
print(f'{WIND_FORCE_THRESHOLD=}')
print(f'{UPDATE_INTERVAL=}')


def discord_number(number: int) -> str:
    emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:',
              ':ten:']

    if 0 <= number < len(emojis):
        return emojis[number]
    else:
        return f'**{str(number)}**'


def update(reading: WeatherReading, last_reading: WeatherReading):
    if reading.timestamp <= last_reading.timestamp:
        print('Ignoring stale data.')
        return

    if reading.wind_force >= WIND_FORCE_THRESHOLD > last_reading.wind_force:
        # Just went above the threshold
        send_discord_message(format_weather_reading(reading,
                                                    f':cloud_tornado: Het is gaan stormen met windkracht **{reading.wind_force}**! :tumbler_glass:'))
    elif reading.wind_force < WIND_FORCE_THRESHOLD <= last_reading.wind_force:
        # Just went below the threshold
        send_discord_message(format_weather_reading(reading, ':cloud: De storm is gaan liggen.'))
    elif reading.wind_force >= WIND_FORCE_THRESHOLD and last_reading.wind_force >= WIND_FORCE_THRESHOLD:
        # Still above the threshold
        if reading.wind_force > last_reading.wind_force:
            # Wind force increased
            send_discord_message(format_weather_reading(reading, ':wind_blowing_face: De windkracht is verhoogd.'))
            pass
        elif reading.wind_force < last_reading.wind_force:
            # Wind force decreased
            send_discord_message(format_weather_reading(reading, ':wind_blowing_face: De windkracht is verlaagd.'))
            pass


def format_weather_reading(reading: WeatherReading, forecast_message: str) -> str:
    return f'{forecast_message}\n\n' + \
        f'> **Windkracht** {discord_number(reading.wind_force)} ({reading.wind_speed} > {reading.wind_gust_speed} m/s)\n' + \
        f'> **Windrichting** {reading.wind_direction_name}\n' + \
        f'> {reading.temperature} °C / {reading.humidity}%\n\n' + \
        f'_(Laatste meting op {reading.timestamp.hour}:{reading.timestamp.minute})_'


def send_discord_message(message: str) -> None:
    print(message)
    DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message).execute()


def main():
    api: WeatherAPI = BuienradarWeatherAPI(
        latitude=LATITUDE,
        longitude=LONGITUDE,
    )

    last_reading: Optional[WeatherReading] = None

    while True:
        reading = api.fetch_reading()
        if reading and last_reading:
            update(reading, last_reading)
        last_reading = reading

        time.sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    main()
