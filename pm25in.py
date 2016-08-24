# -*- coding: utf-8 -*-

import requests
from config import *


class Pm25in(object):
    """
    PM25.in data fetcher
    """
    def __init__(self):
        self.token = PM25IN_TOKEN
        self.base_url = "http://www.pm25.in/api/querys/"
        self.valid_city = [u'上海']

    def get_detail_by_city(self, city_name):
        """
        :param city_name: str / unicode
        :return: JSON object
        """
        if type(city_name) == str:
            city_name = city_name.decode("utf8")
        if city_name not in self.valid_city:
            return None
        final_api = self.base_url + "aqi_details.json"
        r = requests.get(final_api, {'token': self.token, 'city': city_name})
        r.raise_for_status()
        return r.json()

