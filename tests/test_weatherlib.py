#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from weatherlib import WeatherLib


def test_init():
    """test init"""
    WeatherLib('abcde')


def test_get_precipitation(mocker):
    """test get_precipitation"""
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    resp_temp = {
        'Feature': [
            {
                'Property': {
                    'WeatherList': {
                        'Weather': [
                            {'Type': 'observation', 'Date': '201909232330', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232335', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232340', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232345', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232350', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232355', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240000', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240005', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240010', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240015', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240020', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240025', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240030', 'Rainfall': 0.0},
                        ]
                    }
                }
            }
        ]
    }
    response_mock.text = json.dumps(resp_temp)

    mocker.patch('requests.get').return_value = response_mock
    weatherlib = WeatherLib('abcde')
    result = weatherlib.get_precipitation(location='tokyo')
    assert result.is_rain is False
    assert result.current == resp_temp['Feature'][0]['Property']['WeatherList']['Weather'][0]['Date']
    assert str(result) == json.dumps(resp_temp['Feature'][0]['Property']['WeatherList']['Weather'])
    assert result.detail == _convert_detail_result(resp_temp['Feature'][0]['Property']['WeatherList']['Weather'])


def test_get_precipitation_manual(mocker):
    """test get_precipitation"""
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    resp_temp = {
        'Feature': [
            {
                'Property': {
                    'WeatherList': {
                        'Weather': [
                            {'Type': 'observation', 'Date': '201909232330', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232335', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232340', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232345', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909232350', 'Rainfall': 10.0},
                            {'Type': 'forecast', 'Date': '201909232355', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240000', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240005', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240010', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240015', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240020', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240025', 'Rainfall': 0.0},
                            {'Type': 'forecast', 'Date': '201909240030', 'Rainfall': 0.0},
                        ]
                    }
                }
            }
        ]
    }
    response_mock.text = json.dumps(resp_temp)

    mocker.patch('requests.get').return_value = response_mock
    weatherlib = WeatherLib('abcde')
    result = weatherlib.get_precipitation(latitude=100.0, longitude=100.0)
    assert result.is_rain is True
    assert result.current == resp_temp['Feature'][0]['Property']['WeatherList']['Weather'][0]['Date']
    assert str(result) == json.dumps(resp_temp['Feature'][0]['Property']['WeatherList']['Weather'])
    assert result.detail == _convert_detail_result(resp_temp['Feature'][0]['Property']['WeatherList']['Weather'])


def _convert_detail_result(data):
    ret = []
    for i in range(13):
        ret.append({'time': i*5, 'rain_fall': data[i]['Rainfall']})
    return ret
