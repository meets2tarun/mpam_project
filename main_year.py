import pandas as pd
import numpy as np
from os.path import dirname, join
import os
project_path = os.path.dirname(os.path.abspath(__file__))
# data_path = project_paths
data_path = join(project_path, 'Data')
file_list = ['2015', '2016', '2017', '2018']

#
# Dynamic Data
#
file_name = file_list[0] # reading 2018 Data_Unified.csv
file_path = join(data_path, '{} Data_Unified.csv'.format(file_name))
# file_path = join(data_path, 'Total.csv')

data = pd.read_csv(file_path, parse_dates=['Description'])

DropDown_list = list(data)

#
# Dynamic Data
#
date = DropDown_list.pop(0)
var_name = DropDown_list[0]
#  limit alarm_menu
startTime = data[date].min()  # start time of plot
endTime = data[date].max()  # end time of plot

# yVal = reducedDf[column].values
# xVal = reducedDf['timeStampGMT'].values
# #plt.plot(xVal, yVal, label='linear')
#
# reducedAlarmDf = alarmTable.loc[(alarmTable['timeStampGMT'] >= startTime) & (alarmTable['timeStampGMT'] < endTime) & (alarmTable['Point Description'] == alarmName)]
# print(DropDown_list)
alarm_path = join(data_path, 'allAlarms_2015_2019.csv')
alarmTable = pd.read_csv(alarm_path,parse_dates=['timeStampGMT'])
alarm_list = list(alarmTable['Point Description'].unique())
alarmName = alarm_list[1]

def get_AlarmNreturnVals(alarmTable_original, alarmName, startTime, endTime):
    alarmTable = alarmTable_original.loc[(alarmTable_original['timeStampGMT'] >= startTime) & (alarmTable_original['timeStampGMT'] < endTime)]
    reducedAlarmDf = alarmTable.loc[ (alarmTable['Point Description'] == alarmName)]
    reducedAlarmDf_alarm = reducedAlarmDf.loc[reducedAlarmDf['Alarm Type'] == 'ALARM']
    reducedAlarmDf_return = reducedAlarmDf.loc[reducedAlarmDf['Alarm Type'] == 'RETURN']
    alarm_date = reducedAlarmDf_alarm['timeStampGMT'].values
    return_date = reducedAlarmDf_return['timeStampGMT'].values
    alarm_value = np.ones(alarm_date.shape[0])*1*100
    return_value = np.ones(return_date.shape[0])*1*1.2
    return alarm_date, return_date, alarm_value, return_value

alarm_date, return_date, alarm_value, return_value = get_AlarmNreturnVals(alarmTable, alarmName, startTime, endTime)

from bokeh.io import show
from bokeh.models import ColumnDataSource

source_alarm = ColumnDataSource (dict(
            alarm_dt  = alarm_date,
            alarm_vl = alarm_value,
            ))

source_return = ColumnDataSource (dict(
            return_dt = return_date,
            return_vl = return_value
            ))

# source_alarm = ColumnDataSource (dict(
#             alarm_dt  = alarm_date,
#             alarm_vl = alarm_value,
#             return_dt = return_date,
#             return_vl = return_value
#             ))

source = ColumnDataSource (dict(
            x = data[date],
            y = data[var_name]
            ))

from bokeh.plotting import figure
p = figure(title = file_name,
                plot_height=300, plot_width=1300,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef",x_range=(data[date][1], data[date][10000]))#PLOT_OPTS)

p.line(
    x = 'x',
    y = 'y',
    alpha =0.6,
    source = source)#color = 'pink')
p.circle(x = 'alarm_dt', y = 'alarm_vl' ,color="red",size=20,alpha=0.5,source=source_alarm)
p.circle(x = 'return_dt', y = 'return_vl',color="blue" ,size=20,alpha=0.5,source=source_return)
# ##################################
#  Defining ranger
##################################3333333
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=200, plot_width=1200, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")
from bokeh.models import RangeTool
range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line(
        x = 'x',
        y = 'y',
        alpha = 0.6,
        source=source)#,legend=var_name)
select.circle(x = 'alarm_dt', y = 'alarm_vl' ,color="red",size=20,alpha=0.5,source=source_alarm)
select.circle(x = 'return_dt', y = 'return_vl',color="blue" ,size=20,alpha=0.5,source=source_return)

select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool
# show(p)
from bokeh.models.widgets import PreText, Select
var_menu = Select(value=DropDown_list[0], options= DropDown_list)

def var_change(attrname, old, new):
    var_name = var_menu.value
    # print(var_name)
    var_update()
    return var_name


def var_update():
    var_name = var_menu.value
    source.data = dict(x=data[date], y=data[var_name])
    # return var_name

var_name = var_menu.on_change('value', var_change)

alarm_menu = Select(value=alarm_list[0], options= alarm_list)

def alarm_change(attrname, old, new):
    alarm_name = alarm_menu.value
    startTime = data[date].min()  # start time of plot
    endTime = data[date].max()  # end time of plot
    alarm_date, return_date, alarm_value, return_value = get_AlarmNreturnVals(alarmTable, alarm_name, startTime, endTime)
    source_alarm.data = dict(alarm_dt  = alarm_date,alarm_vl = alarm_value)
    source_return.data = dict(return_dt = return_date,return_vl = return_value)
    # print(var_name)
#    alarm_update()

# def alarm_update():
#     alarm_name = alarm_menu.value
#    startTime = data[date].min()  # start time of plot
#    endTime = data[date].max()  # end time of plot
#    alarm_date, return_date, alarm_value, return_value = get_AlarmNreturnVals(alarmTable, alarm_name, startTime, endTime)
    # source_alarm.data = dict(alarm_dt  = alarm_date,alarm_vl = alarm_value,return_dt = return_date,return_vl = return_value)
    # alarm_date, return_date, alarm_value, return_value = get_AlarmNreturnVals(alarmTable, alarm_name, startTime, endTime)
#    source_alarm.data = dict(alarm_dt  = alarm_date,alarm_vl = alarm_value)
#    source_return.data = dict(return_dt = return_date,return_vl = return_value)
alarm_menu.on_change('value', alarm_change)
#alarm_update()


from bokeh.io import curdoc
from bokeh.layouts import row, column

layout = column(p,select,row(var_menu,alarm_menu))
# layout = column(p,select,var_menu,alarm_menu)
var_update()
curdoc().add_root(layout)
curdoc()

