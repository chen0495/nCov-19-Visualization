import akshare as ak
covid_19_163_df = ak.covid_19_163(indicator="世界历史累计数据")
print(covid_19_163_df)
covid_19_163_df.to_csv("世界历史累计数据.csv")


