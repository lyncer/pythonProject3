from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from datetime import datetime,timedelta
from PyQt5.QtGui import *
import dataset
import Logic
from Sql_connect import Sql
import sqlite3
import pandas as pd


Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数', '实装重车', '调妥时间',
              '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件','挂车时间', '线内作业时间分析','待挂时间分析']

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
        text, okPressed = QInputDialog.getText(self, "添加到站", "请输入要添加的到站名（例如：迁安燕钢）:", QLineEdit.Normal, "")
        if okPressed and text != '':
            with open('quxiang.txt', 'a', encoding='utf-8') as quxiang:
                text = ',' + text
                quxiang.write(text)
            QMessageBox.critical(MainWindow, "注意", "添加成功，请重新进入", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    # ===========================远程读表函数=====================================================================
    def Win_Remote_table_from_huodiao(self,MainWindow, table_model, status_bar,GroupBox):
        text, okPressed = QInputDialog.getText(self, "链接远程表格数据库", "请输入地址（\\IP\共享文件夹名字\数据库名字）:", QLineEdit.Normal,
                                               "")
        if okPressed and text != '':
            dataset_address = "sqlite:///" + text
            conn = sqlite3.connect(text)
            cursor = conn.cursor()
            cursor.execute("select name from sqlite_master where type='table' order by name")
            test_all_tables = cursor.fetchall()
            test_all_tables = [j.strip() for i in test_all_tables for j in i]
            table_name_list = []
            for table_name in test_all_tables:
                try:
                    table_name = datetime.strptime(table_name, '%Y.%m.%d')
                    table_name_list.append(table_name)
                except ValueError:
                    continue
            ls = list(set(table_name_list))
            #   ==用了冒泡排序来排序，其他方法效果一样==
            for j in range(len(ls) - 1):
                for i in range(len(ls) - j - 1):
                    lower = ls[i]
                    upper = ls[i + 1]
                    if lower > upper:
                        ls[i], ls[i + 1] = ls[i + 1], ls[i]
            ls = list(ls)
            ls = [datetime.strftime(name, '%Y.%m.%d') for name in ls]
            # 将ls列表中元素从datetime格式转化为str格式
            print(ls)
            conn.commit()
            conn.close()

            remote_tables_dialog = QDialog()
            lay = QFormLayout(remote_tables_dialog)
            edit1 = QComboBox()
            edit2 = QLineEdit()
            edit2.setPlaceholderText('如需打开指定表格，请填写于此，例如：2021.02.03')
            edit1.addItems(ls[-4:])
            button1 = QPushButton('确定读表')
            button2 = QPushButton('取消')
            lay.addRow(edit1)  # 故障类型下拉菜单
            lay.addRow(edit2)
            lay.addRow(button1)
            lay.addRow(button2)

            def dialog_close():  # 关闭对话框的小函数
                remote_tables_dialog.close()
                GroupBox.setCurrentText(edit1.currentText())

            print(edit1.currentText(), 'edit1.currentText()')
            print(edit2.text(), 'edit2.text()')
            button1.clicked.connect(
                lambda: Logic.Table.read_table(table_model, edit1.currentText(), status_bar, sql_address=dataset_address,Groupbox=GroupBox))
            button2.clicked.connect(dialog_close)
            remote_tables_dialog.exec_()


    def Mac_Remote_table_from_huodiao(self,MainWindow):
        pass

    @staticmethod
    def yesterday_table(table_model,status_bar,table_time=yesterday):
        database = Sql.try_connect_sql(table_model)
        query = QSqlQuery()
        conn = dataset.connect("sqlite:///test.db")
        data_table = conn[table_time]
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
            sentence = "CREATE TABLE " + "'" + table_time + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
            query.exec_(sentence)
            print('成功建立表格 {}'.format(today))
            database.commit()
            database.close()
            Logic.Table.read_table(table_model,table_time,status_bar)
        database.commit()
        database.close()
        QMessageBox.critical( table_model,  "注意", "当前是前日写实，请勿修改",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)


    @staticmethod
    def today_table(table_model,table_time,status_bar,groupbox):
        Logic.Table.read_table(table_model,table_time,status_bar,Groupbox=groupbox)
        print(Logic.Table.test_all_tables)



    @staticmethod
    def Table_analyse(table_model,table_time,status_bar):
        #todo 以此函数建立一个df  分析写实全貌
        analyse_df = Logic.Table.table_to_df(table_model,table_time)
        print(analyse_df)
        analyse_df.to_excel('./表格/shit.xlsx')




    @staticmethod
    def add_row(table_model):
        pass


    @staticmethod
    def test(table_model):
        item = [table_model.currentColumn(),table_model]
        print(table_model.column(item))

