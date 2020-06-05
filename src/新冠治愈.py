import requests
import json
import pandas as pd
import os
import datetime
from pyecharts import options as opts
from pyecharts.charts import *

cities = []

def get_ncov_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    data = requests.get(url).json()['data']
    return data

def flatten_ncov_data():
    all = json.loads(get_ncov_data())
    date = all['lastUpdateTime']
    # 第一层：国家
    china = all['areaTree'][0]['children']  # get China data
    # 第二层：省
    for province in china:
        province_ncov = province['children']
        # 第三层：市
        for city in province_ncov:
            # 输出格式
            city_ncov = {
                '日期': date,
                '省份': province['name'],
                '市': city['name'],
                '新增确认': city['today']['confirm'],
                '累计确认': city['total']['confirm'],
                '累计治愈': city['total']['heal'],
                '累计死亡': city['total']['dead']
            }
            cities.append(city_ncov)

def export_excel():
    cities.clear()
    flatten_ncov_data()
    df = pd.DataFrame(cities)
    # 导出Excel
    path = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(path, 'output.xlsx')
    df.to_excel(output_file)

def render_map_chart():
    cities.clear()
    flatten_ncov_data()
    df = pd.DataFrame(cities)
    pro = list(df["省份"])
    con = list(df["累计确认"])
    hea = list(df["累计治愈"])
    hea_con = []
    pro_name = []
    j = 0
    flag = False
    for i in pro:
        if i in pro_name:
            con_num += con[j]
            hea_num += hea[j]
        else:
            if flag:
                hea_con.append(hea_num/con_num)
            pro_name.append(i)
            con_num = con[j]
            hea_num = hea[j]
            flag = True
        j += 1
    hea_con.append(hea_num / con_num)
    map_chart = (
        Map()
            .add("全国疫情", [list(z) for z in zip(pro_name, hea_con)],
                 "china", is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(title_opts=opts.TitleOpts(title="nCoV治愈率地图(" + str(datetime.date.today()) + ")"),
                             legend_opts=opts.LegendOpts(is_show=False),
                             visualmap_opts=opts.VisualMapOpts(max_=1)
                             )
    )
    map_chart.render("nCoV治愈率地图({}).html".format(datetime.date.today()))

if __name__ == "__main__":
    export_excel()
    render_map_chart()
    print("success")