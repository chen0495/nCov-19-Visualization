import json
import time
import requests
from random import random
from countries_ch_to_en import countries_dict

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'
}

def write_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json.dumps(content, ensure_ascii=False))

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    return content

def get_and_save_all_countries():
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    list_total_req = requests.get(url, headers=headers)
    if list_total_req.status_code == 200:
        area_tree = list_total_req.json()['data']['areaTree']
        area_dict = {}
        for area in area_tree:
            country_id = area['id']
            name = area['name']
            area_dict[country_id] = name
        write_file('countries_id_name.json', area_dict)

def get_cy_properties():
    # 获取配置文件信息
    countries_id_name = read_file('countries_id_name.json')
    cy_id_name_dict = json.loads(countries_id_name)
    cy_ch_en = {v: k for k, v in countries_dict.items()}
    cy_id_name_dict['879'] = '波斯尼亚和黑塞哥维那'
    cy_id_name_dict['8102'] = '多哥'
    cy_id_name_dict['8143'] = '刚果民主共和国'
    cy_id_name_dict['95983'] = '刚果'
    cy_id_name_dict['8144'] = '中非'
    cy_id_name_dict['95000011'] = '多米尼加'
    cy_prop = {}
    for key in cy_id_name_dict:
        cy_name = cy_id_name_dict[key]
        if cy_name in cy_ch_en:
            cy_prop[cy_name] = {}
            cy_prop[cy_name]['id'] = key
            cy_prop[cy_name]['en_name'] = cy_ch_en[cy_name]
    return cy_prop

def get_and_save_ncov_data(cy_props):
    url_root = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=%s&t=%s'
    data = []
    for cy_name in cy_props:
        cy_prop = cy_props[cy_name]
        cy_id = cy_prop['id']
        cy_en_name = cy_prop['en_name']
        ts = int(time.time() * 1000)
        url = url_root % (cy_id, ts)
        ncov_req = requests.get(url, headers=headers)
        if ncov_req.status_code != 200:
            print('req error: %s, %s' % (cy_id, cy_name))
            continue
        ncov_collection = {'cy_id': cy_id,
                           'cy_name': cy_name,
                           'cy_en_name': cy_en_name,
                           'data': ncov_req.json()['data']
                           }
        data.append(ncov_collection)
        time.sleep(random() + 1)
    write_file('counties_daily.json', data)

if __name__ == '__main__':
    get_and_save_all_countries()
    cy_props = get_cy_properties()
    get_and_save_ncov_data(cy_props)
    print('success')
