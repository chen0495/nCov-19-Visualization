import csv
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.options.global_options import ThemeType

x_data = []
y_data = []


def process_data():
    with open('湖南省迁出情况.csv', 'r', newline='', encoding='utf-8') as file:
        readers = csv.reader(file)
        data = list(readers)[1:]
        for i in data:
            if i[2] not in x_data:
                x_data.append(i[2])
                y_data.append(float(i[3]))
            else:
                y_data[x_data.index(i[2])] += float(i[3])
    #print(len(x_data))
    #print(y_data)


def draw():
    bar = (
        Bar(init_opts=opts.InitOpts(bg_color='',
                                    width='1400px',
                                    height='700px',
                                    page_title='湖南省迁出图',
                                    theme=ThemeType.DARK
                                    )
            )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(yaxis_data=y_data, series_name='')
            .set_global_opts(title_opts=opts.TitleOpts(title="湖南省迁出图", subtitle=""), xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":30}))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    bar.render('湖南省迁出图.html')


if __name__ == '__main__':
    process_data()
    draw()