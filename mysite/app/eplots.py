from pyecharts.charts import *
from pyecharts.components import *
from pyecharts.options import *
from pyecharts.commons.utils import JsCode
import pyecharts.options as opts
from pyecharts.globals import ThemeType
class SimplePlot():
    x = None
    y = None
    x_xiax_name = None
    y_axis_name = None
    title = None
    

def simple_box(x, data, y_axis_name, title):
    """
    箱线图
    """
    plot = Boxplot(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            theme=ThemeType.MACARONS
        )
    )
    plot.add_xaxis(x)
    plot.add_yaxis(y_axis_name, plot.prepare_data(data))
    plot.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger='axis' # 设置触发条件
        ),
        title_opts=opts.TitleOpts( # 设置标题
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
            padding=[5, 0, 0, 0], # 左边距为0
        ),
        yaxis_opts=opts.AxisOpts( # 设置Y轴
            splitline_opts=opts.SplitLineOpts(is_show=True), # 显示分隔线
#             max_=2000
            
        ), 
    )
    return plot

def simple_line(x, y, y_axis_name, title):
    """
    简单的折线图
    """
    plot = Line(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            theme=ThemeType.MACARONS
        )
    )
    plot.add_xaxis(x)
    plot.add_yaxis(y_axis_name, y)
    plot.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger='axis' # 设置触发条件
        ),
        title_opts=opts.TitleOpts( # 设置标题
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
            padding=[5, 0, 0, 0], # 左边距为0
        ),
        legend_opts=opts.LegendOpts( # 设置图例
            textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bold"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=80,
                range_end=100
            )
        ],
        xaxis_opts=opts.AxisOpts( # 设置X轴
            type_='category',
            axislabel_opts=opts.LabelOpts(
                font_size=12, # 设置字体大小
                font_weight="bold",
            ),
        ),
        yaxis_opts=opts.AxisOpts( # 设置Y轴
            axislabel_opts=opts.LabelOpts(
                font_size=12, # 设置字体大小
                font_weight="bold",
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True), # 显示分隔线
        ), 
    )
    return plot

def simple_bar(x, y, y_axis_name, title):
    """
    简单的柱状图
    """
    plot = Bar(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            theme=ThemeType.MACARONS
        )
    )
    plot.add_xaxis(x)
    plot.add_yaxis(y_axis_name, y)
    plot.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger='axis' # 设置触发条件
        ),
        title_opts=opts.TitleOpts( # 设置标题
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
            padding=[5, 0, 0, 0], # 左边距为0
        ),
    )
    return plot


def simple_pie(data, title):
    """
    简单的饼图
    """
    plot = Pie(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            theme=ThemeType.MACARONS
        )
    )
    plot.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        toolbox_opts=opts.ToolboxOpts(),
    )
    plot.add('', data)
    return plot

def simple_map_china(name, data, title, _max=1000):
    """
    中国地图
    """
    plot = Map(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            theme=ThemeType.MACARONS
        ), 
    )
    plot.add(
        name, 
        data, 
        "china",
        is_map_symbol_show=True,
        label_opts=opts.LabelOpts(
            font_size=10, # 设置字体大小
        ),
        layout_size='100%', # 设置地图大小
        layout_center=['50%', '50%'], # 设置地图中心在屏幕中的位置
    )
    plot.set_global_opts(
        title_opts=opts.TitleOpts(
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
            padding=[5, 0, 0, 0], # 左边距为0
        ), 
        legend_opts=opts.LegendOpts( # 设置图例
            textstyle_opts=opts.TextStyleOpts(font_size=10, font_weight="bold"),
        ),
        visualmap_opts=opts.VisualMapOpts(
            min_=1, 
            max_=_max,
            # is_piecewise=True,
            # pieces=[
            #     {"min": 1, "max": 1000},
            #     {"min": 1000, "max": 3000},
            #     {"min": 3000, "max": 10000},
            #     {"min": 10000, },
            # ],
            textstyle_opts=opts.TextStyleOpts(font_size=10, font_weight="bold"), # 设置字体
            pos_left='left', # 设置到左侧的距离
            pos_bottom='15%', # 距离到顶部的距离
        ),
    )
    return plot

def multi_line(x, data, title):
    """
    符合折线图
    """
    plot = Line(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            theme=ThemeType.MACARONS
        )
    )
    plot.add_xaxis(x)
    for y_axis_name, y in data.items():
        plot.add_yaxis(y_axis_name, y)
        
    plot.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger='axis' # 设置触发条件
        ),
        title_opts=opts.TitleOpts( # 设置标题
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
            padding=[5, 0, 0, 0], # 左边距为0
        ),
        legend_opts=opts.LegendOpts( # 设置图例
            textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bold"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=80,
                range_end=100
            )
        ],
        xaxis_opts=opts.AxisOpts( # 设置X轴
            type_='category',
            axislabel_opts=opts.LabelOpts(
                font_size=12, # 设置字体大小
                font_weight="bold",
            ),
        ),
        yaxis_opts=opts.AxisOpts( # 设置Y轴
            axislabel_opts=opts.LabelOpts(
                font_size=12, # 设置字体大小
                font_weight="bold",
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True), # 显示分隔线
        ), 
    )
    return plot

def multi_bar(x, data, title, stack="stack"):
    """
    复合柱状图
    """
    plot = Bar(
        init_opts=opts.InitOpts(
            width='100%',
            height='500px',
            # 
        )
    )
    plot.add_xaxis(x)
    for y_axis_name, y in data.items():
        plot.add_yaxis(y_axis_name, y, stack=stack)
        
    plot.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger='axis' # 设置触发条件
        ),
        title_opts=opts.TitleOpts( # 设置标题
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
            padding=[5, 0, 0, 0], # 左边距为0
        ),
        legend_opts=opts.LegendOpts( # 设置图例
            textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bold"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=0,
                range_end=100
            )
        ],
        xaxis_opts=opts.AxisOpts( # 设置X轴
            type_='category',
            axislabel_opts=opts.LabelOpts(
                font_size=12, # 设置字体大小
                font_weight="bold",
            ),
        ),
        yaxis_opts=opts.AxisOpts( # 设置Y轴
            axislabel_opts=opts.LabelOpts(
                font_size=12, # 设置字体大小
                font_weight="bold",
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True), # 显示分隔线
        ), 
    )
    return plot



def simple_word_cloud(series_name, data, title):
    """
    词云
    """
    plot = WordCloud(
        init_opts=opts.InitOpts(
            width='100%',
            height='600px',
            theme=ThemeType.MACARONS
        )
    )
    plot.add(series_name, data_pair=data, word_size_range=[10, 66])
    plot.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        toolbox_opts=opts.ToolboxOpts(),
    )
    return plot

def simple_radar(schema, data, title):
    """
    简单雷达图
    schema: [['名称', _max],]
    data: {"名称": [值]}
    """
    plot = Radar(init_opts=opts.InitOpts(width='100%',
                                        height='600px',))
    _schema = []
    for name, _max in schema:
        _schema.append(opts.RadarIndicatorItem(name=name, max_=_max))
    plot.add_schema(
        schema=_schema,
        splitarea_opt=opts.SplitAreaOpts(
            is_show=True,
            areastyle_opts=opts.AreaStyleOpts(opacity=1)
        ),
        textstyle_opts=opts.TextStyleOpts(color="black"),
    )   
    for series_name, _data in data.items():
        # linestyle_opts=opts.LineStyleOpts(color="#5CACEE"),
        plot.add(series_name=series_name, data=[_data])
    plot.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    plot.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        legend_opts=opts.LegendOpts(is_show=True,textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bold"),)
    )
    return plot

# def simple_geo(data, date):
#     """
#     简单地图
#     参考https://blog.csdn.net/zengbowengood/article/details/104695205
#     """
#     plot = Geo(init_opts=opts.InitOpts(
#                 width='100%',
#                 height='600px',
#                 theme=ThemeType.MACARONS
#             ))
#         plot.add_schema(maptype="上海") #限定上海市范围
#         data_pair = []
#         index = 1
#         for x, y in data[['x', 'y']].values:
#             plot.add_coordinate(f"{index}", float(x), float(y)) #追加点位置
#             data_pair.append((f"{index}", 1))
#             index += 1
#         plot.add("", data_pair, symbol_size=2) #追加项目名称和租金
#         plot.set_series_opts(label_opts=opts.LabelOpts(is_show=False), type='scatter')  #星散点图scatter
#         plot.set_global_opts(
#             tooltip_opts=opts.TooltipOpts(
#                 trigger='axis' # 设置触发条件
#             ),
#             title_opts=opts.TitleOpts( # 设置标题
#                 title=f"{date}汽车位置",
#                 title_textstyle_opts=opts.TextStyleOpts(font_size=15, font_weight="bolder"), # 设置字体
#                 padding=[5, 0, 0, 0], # 左边距为0
#             )
#         )

def simple_funnel(data, series_name, title):
    """
    漏斗图
    参考：https://gallery.pyecharts.org/#/Funnel/funnel_chart
    """
    plot = Funnel(init_opts=opts.InitOpts(width="100%", height="600px",theme = ThemeType.PURPLE_PASSION ))
    plot.add(
        series_name,
        data,
        sort_="descending",
        label_opts=opts.LabelOpts(position="inside"),
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
    )
    plot.set_global_opts(title_opts=opts.TitleOpts(title=title))
    return plot
    