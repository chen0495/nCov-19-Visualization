import requests
from pyquery import PyQuery as pq
import json
import pandas as pd
import time

url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
response = requests.get(url)
if response.status_code == 200:
    response.encoding = "utf-8"
    dom = pq(response.content)
    data = dom("script#getAreaStat").text().split(" = ")[1].split("}catch")[0]
    jsonobj = json.loads(data)  # json对象
    print("数据抓取成功...")
province_data = []
for item in jsonobj:
    dic = {}
    dic["省全称"] = item["provinceName"]
    dic["省简称"] = item["provinceShortName"]
    dic["现存确诊人数"] = item["currentConfirmedCount"]
    dic["累计确诊人数"] = item["confirmedCount"]
    dic["疑似人数"] = item["suspectedCount"]
    dic["治愈人数"] = item["curedCount"]
    dic["死亡人数"] = item["deadCount"]
    province_data.append(dic)
if (province_data.__len__() > 0):
    print("写入数据...")
    try:
        df = pd.DataFrame(province_data)
        time_format = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        df.to_csv(time_format + "全国各省疫情数据.csv", encoding="gbk", index=False)
        print("写入成功...")
    except:
        print("写入失败....")
