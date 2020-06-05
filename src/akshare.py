# -*- coding: utf-8 -*-
# @Time    : 2020/5/30 12:14
# @Author  : Chen0495
# @Email   : 1346565673@qq.com|chenweiin612@gmail.com
# @File    : datahelp1.py
# @Software: PyCharm


import akshare as ak

# 利用akshare项目对数据进行补充,数据保存在'/data/csv/'

# 中国疫情防控医院
def hospital():
    covid_19_dxy_df = ak.covid_19_dxy(indicator="中国疫情防控医院")
    print(covid_19_dxy_df)
    covid_19_dxy_df.to_csv(r'../Data/csv/ak中国疫情防控医院.csv', encoding='utf-8')

# 中国实时数据
def cn_real():
    covid_19_163_df = ak.covid_19_163(indicator="中国实时数据")
    print(covid_19_163_df)
    covid_19_163_df.to_csv(r'../Data/csv/ak中国实时数据.csv', encoding='utf-8')

# 中国历史每日新增数据
def cn_new():
    covid_19_163_df = ak.covid_19_163(indicator="中国历史时点数据")
    print(covid_19_163_df)
    covid_19_163_df.to_csv(r'../Data/csv/ak中国历史时点数据.csv', encoding='utf-8')

# 中国历史每日累计数据
def cn_total():
    covid_19_163_df = ak.covid_19_163(indicator="中国历史累计数据")
    print(covid_19_163_df)
    covid_19_163_df.to_csv(r'../Data/csv/ak中国历史累计数据.csv', encoding='utf-8')

# 世界历史时点数据
def global_real():
    covid_19_163_df = ak.covid_19_163(indicator="世界历史时点数据")
    print(covid_19_163_df)
    covid_19_163_df.to_csv(r'../Data/csv/ak世界历史时点数据.csv', encoding='utf-8')

# 世界历史每日累计数据
def global_real():
    covid_19_163_df = ak.covid_19_163(indicator="世界历史累计数据")
    print(covid_19_163_df)
    covid_19_163_df.to_csv(r'../Data/csv/ak世界历史累计数据.csv', encoding='utf-8')