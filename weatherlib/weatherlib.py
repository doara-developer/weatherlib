#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

from .models.precipitation import Precipitation

LOCATION_TEMPLATE = {
    'sapporo': [141.350755, 43.068661],
    'sendai': [140.882438, 38.260132],
    'tokyo': [139.767125, 35.681236],
    'mishima': [138.911126, 35.126299],
    'nagoya': [136.881537, 35.170915],
    'kanazawa': [136.648171, 36.578044],
    'osaka': [135.495951, 34.702485],
    'hakata': [130.420727, 33.589728],
    'naha': [127.652184, 26.206481]
}


class WeatherLib():
    """WeatherLib
    Get weather information by using yahoo api

    Attributes:
    id (str): application id for yahoo api
    """
    id = ''
    url = "https://map.yahooapis.jp/weather/V1/place"

    def __init__(self, id):
        self.id = id

    def get_precipitation(self, location=None, latitude=0.0, longitude=0.0, interval=5):
        """
        Get precipitation for specified location.

        Args:
        location (str): location name.
        latitude (float): location latitude. If set 'location', this parameter is ignored.
        longitude (float): location longitude. If set 'location', this parameter is ignored.

        Returns:
        Precipitation: precipitation info
        """
        if location is not None and location in LOCATION_TEMPLATE:
            coordinates = str(LOCATION_TEMPLATE[location][0]) + ',' + str(LOCATION_TEMPLATE[location][1])
        else:
            coordinates = str(latitude) + ',' + str(longitude)

        payload = {
            'coordinates': coordinates,
            'appid': self.id,
            'output': 'json',
            'interval': str(interval)
        }
        r = requests.get(self.url, params=payload)
        data = json.loads(r.text)

        return Precipitation(data['Feature'][0]['Property']['WeatherList']['Weather'])
