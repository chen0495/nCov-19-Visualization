# -*- coding: utf-8 -*-
# @Time    : 2020/5/3 10:38
# @Author  : Chen0495
# @Email   : 1346565673@qq.com|chenweiin612@gmail.com
# @File    : citydata.py
# @Software: PyCharm


from pyecharts import options as opts
from pyecharts.charts import Line
from datahandle import Data_clear as dc
from pyecharts.globals import ThemeType

# 作图函数
def bar_datazoom_slider(dx, dy,name) -> Line:
    # 设置图参
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION,height='700px'))
            .add_xaxis(dx)
            .add_yaxis('', [])
            .set_global_opts(
            title_opts=opts.TitleOpts(title=name+'疫情'), # 标题
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"), # 工具提示
            yaxis_opts=opts.AxisOpts(   # y轴
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False), # x轴
            datazoom_opts=[opts.DataZoomOpts(is_show=True,)],   # 底部滑动条
            toolbox_opts=opts.ToolBoxFeatureBrushOpts() #工具箱
        )
    )
    ns = ['累计确诊量', '累计治愈量', '累计死亡量']
    cs = ['#FF3300', '#00FF00', '#A2A2A2']
    count = 0
    for i in dy:
        c.add_yaxis(series_name=ns[count], y_axis=dy[count],is_smooth=True,
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color=cs[count]))
        count = count + 1
    return c

if __name__=='__main__':
    names=input('输入你要查询的省(可以多个，空格分隔，注意全称如 湖南省)： ')
    namelist=names.split(" ")

    # 将数据处理为作图函数可接受的格式
    for name in namelist:
        y = []
        for i in range(3):
            y.append([])
        x = []
        province = [name]
        data = dc().area(province)
        print(data[0])
        data = data[0].drop_duplicates().reset_index(drop=True)

        for i, j in data.iterrows():
            y[0].append(j['province_confirmedCount'])
            y[1].append(j['province_curedCount'])
            y[2].append(j['province_deadCount'])
            x.append(j['updateTime'])
        # data=data.reset_index(drop=True)
        for i in range(3):
            y[i]=list(reversed(y[i]))

        # 作图
        Map = bar_datazoom_slider(list(reversed(x)), y,name)
        Map.render(r'../html/'+str(name)+'疫情线图'+'.html')
