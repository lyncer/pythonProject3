import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from datetime import datetime,timedelta
import dataset
import pandas as pd
import sqlite3
from PyQt5 import QtCore



Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数', '实装重车', '调妥时间',
              '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件','挂车时间', '线内作业时间分析','待挂时间分析']

Today = datetime.today()
# 定义today 为“2020.xx.xx”格式的字符串
today =  Today.strftime('%Y.%m.%d')
tomorrow = Today + timedelta(days=1)
tomorrow = tomorrow.strftime('%Y.%m.%d')
#=======================================================================================================================


def time_format(DataFrame):
    DataFrame.replace(regex=r'[:/-]', value='.', inplace=True)
    DataFrame.replace(regex=u'：', value='.', inplace=True)
    return DataFrame