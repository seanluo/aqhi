# -*- coding:utf8 -*-

import math
from pm25in import Pm25in
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def rename_null_to_city_name(city_name, details):
    if type(city_name) == str:
        city_name = city_name.decode("utf8")
    temp = {}
    for x in details:
        if x[u"position_name"]:
            temp[u"监测站:" + x[u"position_name"]] = x
        else:
            x[u"station_code"] = u"shanghai"
            temp[u"城市:" + city_name] = x
    return temp


def calc_aqhi(site_data):
    tp = site_data[1][u'time_point']
    time_point = u"{}年{}月{}日{}时".format(tp[:4], tp[5:7], tp[8:10], tp[11:13])
    aqhi = {'time_point': time_point}
    result = int(round((math.exp(site_data[1]['o3_8h'] * 0.00009) +
                        math.exp(site_data[1]['no2_24h'] * 0.000664) +
                        math.exp(site_data[1]['pm2_5_24h'] * 0.000172) -
                        3) * 100 * 10/15))
    aqhi['value'] = result
    return aqhi


def rank_and_suggestion(aqhi):
    if aqhi in [0, 1, 2]:
        return [u"可忽略", u" 敏感人群- 户外活动一般可正常进行\n 一般人群– 适宜进行户外活动"]
    if aqhi == 3:
        return [u"低", u" 敏感人群- 心肺系统疾病患者应考虑减少户外活动\n 一般人群– 可进行正常户外活动"]
    if aqhi in [4, 5, 6]:
        return [u"中等", u" 敏感人群- 老年人、儿童和心肺系统疾病患者应减少户外活动\n 一般人群– 若出现心肺系统不适症状，则应考虑减少户外活动"]
    if aqhi in [7, 8, 9]:
        return [u"高", u" 敏感人群- 老年人、儿童和心肺系统疾病患者应避免户外活动\n 一般人群– 所有人均应考虑减少户外活动"]
    if aqhi == 10:
        return [u"严重", u" 敏感人群- 所有敏感个体均应杜绝户外活动\n 一般人群– 所有人均应避免户外活动"]

    return "error"


def calc_and_cache_for_list(sites_data):
    for site in sites_data.items():
        aqhi = calc_aqhi(site)
        rank, suggestion = rank_and_suggestion(aqhi['value'])
        msg = u'{} {}\nAQHI指数:{}\n风险等级:{}\n防护建议:\n{}'.format(
                site[0], aqhi['time_point'], aqhi['value'], rank, suggestion)
        try:
            os.mkdir("sites_txt")
        except OSError:
            pass
        with open("sites_txt/%s.txt" % site[1][u'station_code'], "w") as f:
            f.write(msg)


def main():
    city_name = "上海"
    p = Pm25in()
    details = p.get_detail_by_city(city_name)
    site_list = rename_null_to_city_name(city_name, details)
    calc_and_cache_for_list(site_list)


if __name__ == "__main__":
    main()
