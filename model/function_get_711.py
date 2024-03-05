import requests as rq
import xml.etree.ElementTree as ET

request_url = 'https://emap.pcsc.com.tw/EMapSDK.aspx'
# 要注意，7-11 用的不是 `request.get()`，而是另一種，`request.post()`

# 取得所有大台北地區的縣市名稱
def get_town_name_from_xml(xml:str):
    all_geo_object = ET.fromstring(xml).findall('GeoPosition')
    return [geo_element.find('TownName').text for geo_element in all_geo_object] # type: ignore

def get_towns_name(city_code:str):
    form_data = {
        'commandid' : 'GetTown',
        'cityid'    : city_code,
    }

    response = rq.post(
        url = request_url,
        data = form_data
    )

    return get_town_name_from_xml(response.text)

# 取得完整的店家列表
def get_store_info_from_xml(xml:str):
    """ Given a xml response from a city, retrieve all its important information"""
    all_geo_object = ET.fromstring(xml).findall('GeoPosition')
    return [
                {
                    'Name'      : geo_element.find('POIName').text,
                    'X'         : geo_element.find('X').text,
                    'Y'         : geo_element.find('Y').text,
                    'Address'   : geo_element.find('Address').text
                }
                        for geo_element in all_geo_object
            ] # type: ignore

def get_stores_for_town(city_name:str, town_name:str):
    """ Post request on a town (district), return its list of store data."""
    form_data = {
        'commandid' : 'SearchStore',
        'city'      : city_name,
        'town'      : town_name
    }

    response = rq.post(
        url = request_url,
        data = form_data
    )

    store_info_this_town =  get_store_info_from_xml(response.text)
    for store in store_info_this_town:
        store['city'] = city_name
        store['town'] = town_name
    
    return store_info_this_town