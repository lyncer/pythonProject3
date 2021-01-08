from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from datetime import datetime,timedelta
from PyQt5.QtGui import *
import dataset
import Logic
from Sql_connect import Sql
import sqlite3



Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数', '实装重车', '调妥时间',
              '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件', '挂车时间', '备注']

Today = datetime.today()
# 定义today 为“2020.xx.xx”格式的字符串
today =  Today.strftime('%Y.%m.%d')
tomorrow = Today + timedelta(days=1)
tomorrow = tomorrow.strftime('%Y.%m.%d')
yesterday = Today - timedelta(days=1)
yesterday = yesterday.strftime('%Y.%m.%d')

class Menubar:
    def __init__(self):
        pass

    def save_event(self):
        # todo 待回写函数完成后 再构建这里
        print('shit')

    def addStation(self,MainWindow):
        dialog = QInputDialog()
        edit = QLineEdit(dialog)
        stationName,a = dialog.getText(MainWindow,'对话框','到站名')
        print(stationName)
        dialog.exec_()



    @staticmethod
    def yesterday_table(table_model):
        database = Sql.try_connect_sql(table_model)
        query = QSqlQuery()
        conn = dataset.connect("sqlite:///test.db")
        data_table = conn[yesterday]
        try:
            database_result = data_table.all().result_proxy
            for row_index, row_data in enumerate(database_result):
                for col_index, value in enumerate(row_data[1:]):  # 舍去row_data的第一个元素，是个数字
                    if col_index not in [1, 2]:
                        item = QTableWidgetItem(value)
                        table_model.setItem(row_index, col_index, item)
                    else:
                        table_model.cellWidget(row_index, col_index).setCurrentText(value)
        except AttributeError:
            sentence = "CREATE TABLE " + "'" + today + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
            query.exec_(sentence)
            print('成功建立表格 {}'.format(today))
            print('当前表格列表：', database.tables())
            database.commit()
            database.close()
        database.commit()
        database.close()
        QMessageBox.critical( table_model,  "注意", "当前是前日写实，请勿修改",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)


    @staticmethod
    def today_table(table_model):
        Logic.Table.read_table(table_model)
        print(Logic.Table.test_all_tables,'shit')

    @staticmethod
    def passtable(table_model,status_bar=None):
        button = QMessageBox.critical( table_model,  "注意", "今日写实填写完毕后方可过表操作，确定过表吗？",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
        if button == QMessageBox.Ok:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("select name from sqlite_master where type='table' order by name")
            test_all_tables = cursor.fetchall()
            # 打印出test.db中所有表名
            # cursor.fetchall()输出的格式为：    [('2020.12.11',), ('2020.12.12',), ('2020.12.14',), ('remark_2020.12.14',), ('sqlite_sequence',)]
            test_all_tables = [j for i in test_all_tables for j in
                               i]  # 格式为：['2020.12.11', '2020.12.12', '2020.12.14', 'remark_2020.12.14', 'sqlite_sequence']
            if tomorrow not in test_all_tables:
                # 如果数据库里没有名为today的表
                status_bar.showMessage('成功过表，目前写实日期为' + tomorrow)
                sentence = "CREATE TABLE " + "'" + tomorrow + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
                cursor.execute(sentence)
            else:
                status_bar.showMessage('已存在{}数据表'.format(tomorrow))
                Logic.Table.read_table(table_model,table_time=tomorrow)
                #todo 若保存也是保存到tomorrow才行




    @staticmethod
    def add_row(table_model):
        pass


    @staticmethod
    def test(table_model):
        item = [table_model.currentColumn(),table_model]
        print(table_model.column(item))

