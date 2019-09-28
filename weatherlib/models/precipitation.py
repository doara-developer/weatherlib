#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json


class Precipitation():
    """Precipitation Model
    Precipitation model.

    Attributes:
    data (list): response from yahoo api
    """
    data = []

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return json.dumps(self.data)

    @property
    def current(self):
        return self.data[0]['Date']

    @property
    def is_rain(self):
        return any(elem['Rainfall'] > 0 for elem in self.data)

    @property
    def detail(self):
        cur_date = self._convert_datetime(self.data[0]['Date'])
        ret = [
            {
                'time': int((self._convert_datetime(d['Date']) - cur_date).seconds/60),
                'rain_fall': d['Rainfall']
            }
            for d in self.data
        ]
        return ret

    def _convert_datetime(self, datestr):
        return datetime.datetime.strptime(datestr, '%Y%m%d%H%M')
