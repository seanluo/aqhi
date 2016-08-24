# -*- coding: utf-8 -*-

import requests
from config import *


class CityNameException(Exception):
    pass


class PollutantNameException(Exception):
    pass


class Pm25InResultError(Exception):
    pass


class Pm25in(object):
    """
    PM25.in data fetcher
    """
    def __init__(self):
        self.token = PM25IN_TOKEN
        self.base_url = "http://www.pm25.in/api/querys/"
        self.valid_city = [u"七台河", u"三亚", u"三明", u"三门峡", u"上海", u"上饶", u"东莞", u"东营", u"中卫", u"中山",
                           u"临夏州", u"临安", u"临汾", u"临沂", u"临沧", u"丹东", u"丽水", u"丽江", u"义乌", u"乌兰察布",
                           u"乌海", u"乌鲁木齐", u"乐山", u"九江", u"乳山", u"云浮", u"五家渠", u"亳州", u"伊春",
                           u"伊犁哈萨克州", u"佛山", u"佳木斯", u"保定", u"保山", u"信阳", u"克州", u"克拉玛依", u"六安",
                           u"六盘水", u"兰州", u"兴安盟", u"内江", u"凉山州", u"包头", u"北京", u"北海", u"十堰", u"南京",
                           u"南充", u"南宁", u"南平", u"南昌", u"南通", u"南阳", u"博州", u"即墨", u"厦门", u"双鸭山", u"句容",
                           u"台州", u"合肥", u"吉安", u"吉林", u"吐鲁番地区", u"吕梁", u"吴忠", u"吴江", u"周口", u"呼伦贝尔",
                           u"呼和浩特", u"和田地区", u"咸宁", u"咸阳", u"哈密地区", u"哈尔滨", u"唐山", u"商丘", u"商洛",
                           u"喀什地区", u"嘉兴", u"嘉峪关", u"四平", u"固原", u"塔城地区", u"大兴安岭地区", u"大同", u"大庆",
                           u"大理州", u"大连", u"天水", u"天津", u"太仓", u"太原", u"威海", u"娄底", u"孝感", u"宁德", u"宁波",
                           u"安庆", u"安康", u"安阳", u"安顺", u"定西", u"宜兴", u"宜宾", u"宜昌", u"宜春", u"宝鸡", u"宣城",
                           u"宿州", u"宿迁", u"富阳", u"寿光", u"山南地区", u"岳阳", u"崇左", u"巴中", u"巴彦淖尔", u"常州",
                           u"常德", u"常熟", u"平凉", u"平度", u"平顶山", u"广元", u"广安", u"广州", u"庆阳", u"库尔勒",
                           u"廊坊", u"延安", u"延边州", u"开封", u"张家口", u"张家港", u"张家界", u"张掖", u"徐州", u"德宏州",
                           u"德州", u"德阳", u"忻州", u"怀化", u"怒江州", u"恩施州", u"惠州", u"成都", u"扬州", u"承德",
                           u"抚州", u"抚顺", u"拉萨", u"招远", u"揭阳", u"攀枝花", u"文山州", u"文登", u"新乡", u"新余",
                           u"无锡", u"日喀则地区", u"日照", u"昆山", u"昆明", u"昌吉州", u"昌都地区", u"昭通", u"晋中", u"晋城",
                           u"普洱", u"景德镇", u"曲靖", u"朔州", u"朝阳", u"本溪", u"来宾", u"杭州", u"松原", u"林芝地区",
                           u"果洛州", u"枣庄", u"柳州", u"株洲", u"桂林", u"梅州", u"梧州", u"楚雄州", u"榆林", u"武威",
                           u"武汉", u"毕节", u"永州", u"汉中", u"汕头", u"汕尾", u"江门", u"江阴", u"池州", u"沈阳", u"沧州",
                           u"河池", u"河源", u"泉州", u"泰安", u"泰州", u"泸州", u"洛阳", u"济南", u"济宁", u"海东地区",
                           u"海北州", u"海南州", u"海口", u"海西州", u"海门", u"淄博", u"淮北", u"淮南", u"淮安", u"深圳",
                           u"清远", u"温州", u"渭南", u"湖州", u"湘潭", u"湘西州", u"湛江", u"溧阳", u"滁州", u"滨州", u"漯河",
                           u"漳州", u"潍坊", u"潮州", u"濮阳", u"烟台", u"焦作", u"牡丹江", u"玉林", u"玉树州", u"玉溪",
                           u"珠海", u"瓦房店", u"甘南州", u"甘孜州", u"白城", u"白山", u"白银", u"百色", u"益阳", u"盐城",
                           u"盘锦", u"眉山", u"石嘴山", u"石家庄", u"石河子", u"福州", u"秦皇岛", u"章丘", u"红河州", u"绍兴",
                           u"绥化", u"绵阳", u"聊城", u"肇庆", u"胶南", u"胶州", u"自贡", u"舟山", u"芜湖", u"苏州", u"茂名",
                           u"荆州", u"荆门", u"荣成", u"莆田", u"莱州", u"莱芜", u"莱西", u"菏泽", u"萍乡", u"营口", u"葫芦岛",
                           u"蓬莱", u"蚌埠", u"衡水", u"衡阳", u"衢州", u"襄阳", u"西双版纳州", u"西宁", u"西安", u"许昌",
                           u"诸暨", u"贵港", u"贵阳", u"贺州", u"资阳", u"赣州", u"赤峰", u"辽源", u"辽阳", u"达州", u"运城",
                           u"连云港", u"迪庆州", u"通化", u"通辽", u"遂宁", u"遵义", u"邢台", u"那曲地区", u"邯郸", u"邵阳",
                           u"郑州", u"郴州", u"鄂尔多斯", u"鄂州", u"酒泉", u"重庆", u"金华", u"金坛", u"金昌", u"钦州",
                           u"铁岭", u"铜仁地区", u"铜川", u"铜陵", u"银川", u"锡林郭勒盟", u"锦州", u"镇江", u"长春", u"长沙",
                           u"长治", u"阜新", u"阜阳", u"防城港", u"阳江", u"阳泉", u"阿克苏地区", u"阿勒泰地区", u"阿坝州",
                           u"阿拉善盟", u"阿里地区", u"陇南", u"随州", u"雅安", u"青岛", u"鞍山", u"韶关", u"马鞍山", u"驻马店",
                           u"鸡西", u"鹤壁", u"鹤岗", u"鹰潭", u"黄冈", u"黄南州", u"黄山", u"黄石", u"黑河", u"黔东南州",
                           u"黔南州", u"黔西南州", u"齐齐哈尔", u"龙岩"]
        self.valid_pollutant = ['pm2_5', 'pm10', 'co', 'no2', 'so2', 'o3']

    def _check_city_name(self, city_name):
        """
        :param city_name: str / unicode
        :return: unicode / None
        """
        if type(city_name) == str:
            city_name = city_name.decode("utf8")
        if city_name not in self.valid_city:
            raise CityNameException(city_name)
        return city_name

    @staticmethod
    def _check_json_error(result):
        if type(result) == dict and result["error"]:
            raise Pm25InResultError(result["error"])
        else:
            return result

    def get_pollutant_by_city(self, city_name, pollutant, avg=True):
        """
        pm2_5, pm10, co, no2, so2 -> xx and xx_24h
        o3 -> o3, o3_24h, o3_8h, o3_8h_24h
        frequency limit: 500/hour for each pollutant
        :param city_name: str
        :param pollutant: str
        :param avg: bool, include city average or not, default true
        :return: list[dict_site_details]
        """
        city_name = self._check_city_name(city_name)
        if pollutant not in self.valid_pollutant:
            raise PollutantNameException(pollutant)
        final_api = self.base_url + "%s.json" % pollutant
        r = requests.get(final_api, {'token': self.token, 'city': city_name, 'avg': avg})
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())

    def get_aqi_by_city(self, city_name, avg=True):
        """
        only AQI
        frequency limit: 500/hour
        :param city_name: str
        :param avg: bool, include city average or not, default true
        :return: list[dict_site_details]
        """
        city_name = self._check_city_name(city_name)
        final_api = self.base_url + "only_aqi.json"
        r = requests.get(final_api, {'token': self.token, 'city': city_name, 'avg': avg})
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())

    def get_all_by_city(self, city_name, avg=True):
        """
        data for all pollutants
        frequency limit: 500/hour
        :param city_name: str
        :param avg: bool, include city average or not, default true
        :return: list[dict_site_details]
        """
        city_name = self._check_city_name(city_name)
        final_api = self.base_url + "aqi_details.json"
        r = requests.get(final_api, {'token': self.token, 'city': city_name, 'avg': avg})
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())

    def get_all_by_station_code(self, station_code):
        """
        data for all pollutants
        frequency limit: 500/hour
        :param station_code: str
        :return: list[dict_one_site_details], only one element
        """
        final_api = self.base_url + "aqis_by_station.json"
        r = requests.get(final_api, {'token': self.token, 'station_code': station_code})
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())

    def get_stations_by_city(self, city_name, all_stations=False):
        """
        only AQI
        frequency limit: 15/hour
        :param city_name: str
        :param all_stations: bool, ignore city_name, return all stations in China
        :return: dict{city:xx, stations:list[dict{station_name:yy, station_code:zz}]} / all: list[city_dict]
        """
        if all_stations:
            params = {'token': self.token}
        else:
            city_name = self._check_city_name(city_name)
            params = {'token': self.token, 'city': city_name}
        final_api = self.base_url + "station_names.json"
        r = requests.get(final_api, params=params)
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())

    def get_all(self):
        """
        data for all pollutants in all cities
        frequency limit: 5/hour, invoke with caution!
        :return: list[dict_site_details]
        """
        final_api = self.base_url + "all_cities.json"
        r = requests.get(final_api, {'token': self.token})
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())

    def get_city_ranking(self):
        """
        ranking for cities by AQI ascending
        frequency limit: 15/hour
        :return: ordered list[dict_city_all_pollution_avg]
        """
        final_api = self.base_url + "aqi_ranking.json"
        r = requests.get(final_api, {'token': self.token})
        r.raise_for_status()
        return Pm25in._check_json_error(r.json())
