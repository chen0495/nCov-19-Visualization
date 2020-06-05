import json
import datetime
from pyecharts.charts import Timeline, Map
from pyecharts import options as opts
from datetime import datetime as dt
from China_append_data import china_append_data
from countries_ch_to_en import countries_dict
from pyecharts.options.global_options import ThemeType

def get_date_range(start_date, end_date):
    begin_date = dt.strptime(start_date, '%Y-%m-%d')
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    date_list = []
    tmp_date = begin_date
    while tmp_date <= end_date:
        date_list.append(tmp_date.strftime('%Y-%m-%d'))
        tmp_date += datetime.timedelta(days=1)
    return date_list


def parse_ncov_data(start_date, end_date, records):
    if not records:
        return
    date_list = get_date_range(start_date, end_date)
    cy_name_list = []
    res = {}
    for i, record in enumerate(records):
        cy_name = record['cy_name']
        cy_name_list.append(cy_name)
        existing_case_dict = {}
        for ncov_daily in record['data']['list']:
            date_str = ncov_daily['date']
            confirm = ncov_daily['total']['confirm']  # 累计确诊
            heal = ncov_daily['total']['heal']  # 累计治愈
            dead = ncov_daily['total']['dead']  # 累计死亡
            existing_case = confirm - heal - dead
            existing_case_dict[date_str] = existing_case
        last_existing_case = 0
        for date_str in date_list:
            if date_str not in res:
                res[date_str] = []
            existing_case = existing_case_dict.get(date_str)
            if existing_case is None:
                existing_case = last_existing_case
            res[date_str].append(existing_case)
            last_existing_case = existing_case
    return date_list, cy_name_list, res


def render_map(date_list, cy_name_list, ncov_data) -> Map:
    tl = Timeline()
    tl.add_schema(is_auto_play=True, play_interval=60, is_loop_play=False, width=700)
    for date_str in date_list:
        map_ = (
            Map(init_opts=opts.InitOpts(bg_color='rgba(255,250,205,0.2)',
                                width='1000px',
                                height='600px',
                                page_title='page',
                                theme=ThemeType.MACARONS))
            .add("全球疫情变化", [list(z) for z in zip(cy_name_list, ncov_data[date_str])],
                 "world", is_map_symbol_show=False,
                 name_map=countries_dict)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="19-nCoV\n%s" % date_str),
                             legend_opts=opts.LegendOpts(is_show=False),
                             visualmap_opts=opts.VisualMapOpts(max_=3000))
        )
        tl.add(map_, "%s" % date_str)
    tl.render("nCoV全球疫情地图({}).html".format(datetime.date.today()))



def fix_china_data(records):
    for i in range(len(records)):
        if records[i]['cy_id'] == '0':
            records[i]['data']['list'].extend(china_append_data)
            break

if __name__ == '__main__':
    with open("counties_daily.json", 'r', encoding='utf-8') as f:
        records = json.load(f)
    fix_china_data(records)
    date_p = datetime.datetime.now().date()
    date_list, cy_name_list, res = parse_ncov_data('2020-01-20', str(date_p), records)
    render_map(date_list, cy_name_list, res)
    print('success')
