# from typing import Any
from gridded_data import get_weather_by_type, WeatherDataType, Location


def main():
    get_weather_by_type(WeatherDataType.TMAX, years=[2020], location=Location(21.03, 77.23))

if __name__ == '__main__':
    main()
    