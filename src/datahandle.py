# -*- coding: utf-8 -*-
# @Time    : 2020/5/3 11:24
# @Author  : Chen0495
# @Email   : 1346565673@qq.com|chenweiin612@gmail.com
# @File    : datahandle.py
# @Software: PyCharm

import pandas as pd

# 选取数据中需要的列
Area = ['continentName', 'countryName', 'provinceName', 'province_confirmedCount', 'province_suspectedCount',
        'province_curedCount', 'province_deadCount', 'updateTime', 'cityName', 'city_confirmedCount',
        'city_suspectedCount', 'city_curedCount', 'city_deadCount']
Overall = ['_id', 'currentConfirmedCount', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount',
           'seriousCount', 'suspectedIncr', 'currentConfirmedIncr', 'confirmedIncr', 'curedIncr', 'deadIncr',
           'seriousIncr', 'globalStatistics', 'updateTime']

# 数据清洗
class Data_clear:
    def __init__(self, Anames=Area, Onames=Overall,flag=False):  #flag决定是否对日期时间列做进一步处理，将时分秒转为0方便处理
        self.Adata = pd.read_csv(r'../Data/csv/DXYArea.csv', encoding='utf-8', usecols=Anames, low_memory=False,
                                 header=0)
        self.Adata['updateTime'] = pd.to_datetime(self.Adata['updateTime'])
        if flag==True:
            self.Adata['updateTime']=self.Adata['updateTime'].dt.normalize()
        self.Odata = pd.read_csv(r'../Data/csv/DXYOverall.csv', encoding='utf-8', usecols=Onames, low_memory=False,
                                 header=0)
        self.Odata['updateTime'] = pd.to_datetime(self.Odata['updateTime'])
        if flag==True:
            self.Odata['updateTime']=self.Odata['updateTime'].dt.normalize()
        self.Adata = self.Adata.reset_index(drop=True)
        self.Odata = self.Odata.reset_index(drop=True)

    def area(self, name=[]):  # 地区名包括国家和省市
        result = []
        for i in name:
            result.append(
                self.Adata[['continentName', 'countryName', 'provinceName', 'province_confirmedCount',
                            'province_suspectedCount',
                            'province_curedCount', 'province_deadCount', 'updateTime']][
                    self.Adata['provinceName'] == i])  # 国家数据的省名与国名相同
        return result

    def city(self, name=[]):  # 城
        result = []
        for i in name:
            result.append(self.Adata[['continentName', 'countryName', 'provinceName', 'cityName', 'city_confirmedCount',
                                      'city_suspectedCount', 'city_curedCount', 'city_deadCount', 'updateTime']][
                              self.Adata['cityName'] == i])
        return result

    def overall(self):  # 全球总数据
        return self.Odata
