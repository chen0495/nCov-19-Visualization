# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 16:09
# @Author  : Chen0495
# @Email   : 1346565673@qq.com|chenweiin612@gmail.com
# @File    : calendar.py
# @Software: PyCharm

from pyecharts import options as opts
import datahandle as dh
from pyecharts.charts import Calendar as Cal
import csv
import pandas as pd
import datetime

# 作图函数
def Calmap(name, data,maxnum,minnum):
    c = (
        Cal()
            .add(
            "",
            data,
            calendar_opts=opts.CalendarOpts(
                range_="2020",
                daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=name + '疫情日历图'),
            visualmap_opts=opts.VisualMapOpts(
                max_=maxnum,
                min_=minnum,
                orient="horizontal",
                is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
            ),
        )
            .render(name + '疫情日历图.html')
    )


if __name__ == '__main__':
    names = input('输入你要查询的省(可以多个，空格分隔，注意全称如 湖南省)： ')
    names = names.split(" ")
    data = dh.Data_clear(flag=True)  # 启用数据日期处理
    datas = data.area(name=names)
    for i in datas:
        i = i.drop_duplicates().reset_index(drop=True)
    count = -1
    fd = []
    for name in names:
        count += 1
        # 写入数据，保存以方便查看,路径为'/Data/csv/name_daily.csv'
        with open(r'../Data/csv/' + name + '_daily.csv', 'w', encoding='utf8') as f:
            csv_w = csv.writer(f)
            csv_w.writerow(
                ['continentName', 'countryName', 'provinceName', 'province_confirmedCount', 'province_suspectedCount',
                 'province_curedCount', 'province_deadCount', 'updateTime'])
            for i, j in datas[count].iterrows():
                if tuple([j['provinceName'], j['updateTime']]) in fd:
                    continue
                else:
                    fd.append(tuple([j['provinceName'], j['updateTime']]))
                    csv_w.writerow(j)

    datas = []
    for name in names:
        i = pd.read_csv(r'../Data/csv/' + name + '_daily.csv', encoding='utf-8', low_memory=False, header=0) #数据文件过大，将low_memory置为False
        '''
        begin = [int(j) for j in max(list(i['updateTime'])).split(" ")[0].split('-')]
        end = [int(j) for j in min(list(i['updateTime'])).split(" ")[0].split('-')]
        begin=datetime.date(begin[0],begin[1],begin[2])
        end=datetime.date(end[0],end[1],end[2])
        '''
        data = []
        maxnum=max(i['province_confirmedCount'])
        minnum=min(i['province_confirmedCount'])

        # 将数据处理为作图函数可接受的格式
        for j,k in i.iterrows():
            string=[int(n) for n in str(k['updateTime']).split(" ")[0].split("-")]
            string=datetime.date(string[0],string[1],string[2])
            num=k['province_confirmedCount']
            data.append([string,num])
        Calmap(data=data, name=name,maxnum=maxnum,minnum=minnum)
