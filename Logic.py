import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQuery
from datetime import datetime
import dataset
import pandas as pd
import sqlite3
from PyQt5 import QtCore

Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数', '实装重车', '调妥时间',
              '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件','挂车时间', '备注']

Today = datetime.today()
# 定义today 为“2020.xx.xx”格式的字符串
today = '.'.join(map(str, [Today.year, Today.month, Today.day]))
tomorrow = '.'.join(map(str, [Today.year, Today.month, Today.day+1]))


class Table:
    def __init__(self):
        pass

    def init_sql(self):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("select name from sqlite_master where type='table' order by name")
        test_all_tables = cursor.fetchall()
        # 打印出test.db中所有表名
        # cursor.fetchall()输出的格式为：    [('2020.12.11',), ('2020.12.12',), ('2020.12.14',), ('remark_2020.12.14',), ('sqlite_sequence',)]
        test_all_tables = [j for i in test_all_tables for j in i] # 格式为：['2020.12.11', '2020.12.12', '2020.12.14', 'remark_2020.12.14', 'sqlite_sequence']
        if today not in  test_all_tables:
            #如果数据库里没有名为today的表
            print(f'没找到{today},重新建表')
            sentence = "CREATE TABLE " + "'" + today + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
            cursor.execute(sentence)
        else:
            pass


    @staticmethod
    def read_table(table_model):
        database = QSqlDatabase.addDatabase('QSQLITE')
        database.setDatabaseName('test.db')
        if not database.open():
            print('数据库建立失败')
        else:
            query = QSqlQuery()
            # 若数据库中不存在tomorrow的数据表则将其删除，并打印"成功删除"
            if tomorrow not in database.tables():
                print('不存在{}'.format(tomorrow),'准备反写',today)
                #todo 反写数据至model
                conn = dataset.connect("sqlite:///test.db")
                data_table = conn[today]
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



            # 将today设为数据表的名字,建立完整的数据表
            else:
                print('存在{}'.format(tomorrow), '准备反写', tomorrow)
                # todo 反写数据至model
                conn = dataset.connect("sqlite:///test.db")
                data_table = conn[tomorrow]
                database_result = data_table.all().result_proxy
                for row_index, row_data in enumerate(database_result):
                    for col_index, value in enumerate(row_data[1:]):  # 舍去row_data的第一个元素，是个数字
                        if col_index not in [1, 2]:
                            item = QTableWidgetItem(value)
                            table_model.setItem(row_index, col_index, item)
                        else:
                            table_model.cellWidget(row_index, col_index).setCurrentText(value)




class Remarks:
    def __init__(self):
        pass

    def show_dialog(self,remark_button):
        # database = QSqlDatabase.addDatabase('QSQLITE')
        # database.setDatabaseName('test.db')
        # if not database.open():
        #     print('数据库建立失败')
        # else:
        #     remark_today = 'remark_' + today
        #     query = QSqlQuery()
        #     # 若数据库中已经存在名为today的数据表则将其删除，并打印"成功删除"
        #     if today in database.tables():
        #         sentence = "DROP TABLE" + " " + "'" + remark_today + "'"
        #         print(sentence)
        #         query.exec_(sentence)
        #         print('成功删除表 {}'.format(today))
        #         print(database.tables())
        #     # 将today设为数据表的名字,建立完整的数据表
        #     sentence = "CREATE TABLE " + "'" + remark_today + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
        #     query.exec_(sentence)
        #
        #     conn = dataset.connect("sqlite:///test.db")
        #     # 注意路径格式
        #     data_table = conn[today]
        #     print('成功建立表格 {}'.format(today))
        #     print('当前表格列表：', database.tables())
        #     database.close()
        conn = sqlite3.connect('test.db')


        remark_dialog = QDialog()
        lay = QFormLayout(remark_dialog)

        edit1 = QComboBox()
        edit1.addItems(['设备故障','混配卸船','天气因素'])
        edit2 = QLineEdit()
        edit2.setPlaceholderText('时间')
        edit3 = QTextEdit()


        lay.addRow(edit1)
        lay.addRow(edit2)
        lay.addRow(edit3)
        print(remark_button.sender().pos())
        remark_dialog.exec_()


class MyVersionQTableWidget(QTableWidget):
    def __init__(self):
        super(MyVersionQTableWidget, self).__init__()

    def keyPressEvent(self, event):
        super(MyVersionQTableWidget, self).keyPressEvent(event)
        if event.key() == 16777220:
            self.focusNextChild()

