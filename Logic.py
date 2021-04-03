from PyQt5.QtWidgets import *
import dataset
import os
import pandas as pd
import sqlite3
from PyQt5 import QtCore
from Sql_connect import Sql
from datetime import datetime,timedelta

Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数', '实装重车', '调妥时间',
              '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件','挂车时间', '线内作业时间分析','待挂时间分析']

Today = datetime.today()
# 定义today 为“2020.xx.xx”格式的字符串
today = Today.strftime('%Y.%m.%d')
tomorrow = Today + timedelta(days=1)
tomorrow = tomorrow.strftime('%Y.%m.%d')


class Table:
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table' order by name")
    test_all_tables = cursor.fetchall()
    conn.commit()
    conn.close()
    # 打印出test.db中所有表名
    # cursor.fetchall()输出的格式为：    [('2020.12.11',), ('2020.12.12',), ('2020.12.14',), ('remark_2020.12.14',), ('sqlite_sequence',)]
    test_all_tables = [j for i in test_all_tables for j in
                       i]  # 格式为：['2020.12.11', '2020.12.12', '2020.12.14', 'remark_2020.12.14', 'sqlite_sequence']

    def __init__(self):
        pass

    def init_sql(self):
        if today not in Table.test_all_tables:
            # 如果数据库里没有名为today的表
            print('没找到{},重新建表'.format(today))
            sentence = "CREATE TABLE " + "'" + today + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            try:
                cursor.execute(sentence)
            except sqlite3.OperationalError:
                print('sqlite3.OperationalError:%s 已经存在'%today)
            finally:
                conn.commit()
                conn.close()
        else:
            pass

    @staticmethod
    def read_table(table_model, table_time, status_bar,sql_address="sqlite:///test.db",Groupbox=None):
        database = Sql.try_connect_sql(table_model)
        conn = dataset.connect(sql_address)
        data_table = conn[table_time]
        database_result = data_table.all().result_proxy
        if database_result.fetchall():
            database_result = data_table.all().result_proxy

            # result_proxy 对象的 fetchall方法  可以检查是否为空表
            try:
                for row_index, row_data in enumerate(database_result):
                    for col_index, value in enumerate(row_data[1:]):  # 舍去row_data的第一个元素，是个数字
                        if col_index not in [1, 2]:
                            item = QTableWidgetItem(value)
                            table_model.setItem(row_index, col_index, item)
                        else:
                            table_model.cellWidget(row_index, col_index).setCurrentText(value)
            except:
                status_bar.showMessage('出现问题')
                # except AttributeError:
                #     sentence = "CREATE TABLE " + "'" + table_time + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
                #     query.exec_(sentence)
                #     print('成功建立表格 {}'.format(table_time))
            conn.commit()
            conn.close()
        else:
            QMessageBox.critical(table_model, "注意", "{}无数据".format(table_time), QMessageBox.Ok | QMessageBox.Cancel,
                                 QMessageBox.Ok)
            # =====抹除当前页面数据的函数=======================
            value = 0
            for row_index, row_data in enumerate(list(range(26))):
                for col_index in list(range(17)):  # 舍去row_data的第一个元素，是个数字
                    if col_index not in [0, 1, 2]:
                    # 若列索引不是 0 ，1，2
                        item = QTableWidgetItem('')
                        table_model.setItem(row_index, col_index, item)
                    elif col_index == 0:
                        work_location = ['实业一期', '实业一期', '实业一期', '实业一期', '实业一期', '实业一期', '实业一期', '实业一期',
                                     '实业二期', '实业二期', '实业二期', '实业二期', '实业二期', '实业二期','实业二期','实业二期', '实业二期','矿三', '矿三',
                                     '矿三', '矿三', '矿三', '矿三', '矿三', '矿三', '矿三']
                        item = QTableWidgetItem(work_location[value])
                        table_model.setItem(row_index, col_index, item)
                        value += 1
                    elif col_index == 1 or col_index == 2:
                        table_model.cellWidget(row_index,col_index).setCurrentIndex(0)

            # =====抹除当前页面数据的函数 ======================
        status_bar.showMessage(table_time)
        if Groupbox:
            # 如果传入了Groupbox参数 则修改其currentText
            Groupbox.setCurrentText(table_time)


    @staticmethod
    def table_to_df(table,table_time):
    #定义将Table控件转为pandas Dataframe类型的函数
        row_table = []
        for row_num in range(26):
            # row_num 是0-23（表格的行数）
            row_data = []
            for col_num, col_name in enumerate(Head_label):
                # col_num 是0-14（表格的列数）
                try:
                    widget_content = table.cellWidget(row_num, col_num).currentText()
                    row_data.append(widget_content)
                    # 表格的控件内容
                except AttributeError:
                    try:
                        widget_content = table.item(row_num, col_num).text()
                        row_data.append(widget_content)
                        # 表格的非控件内容
                    except AttributeError:
                        row_data.append('')
            row_table.append(row_data)
        table_df = pd.DataFrame(row_table)
        table_df.columns = Head_label
        # ==数据清洗===
        table_df.replace(regex=r'\.', value=':', inplace=True)
        table_df.replace(regex=u'：', value=':', inplace=True)
        # 转化为时间格式
        time_col_list = ['调妥时间', '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件', '挂车时间']
        for time_col_name in time_col_list:
            table_df[time_col_name] = pd.to_datetime(table_df[time_col_name], format='%H:%M', errors='ignore')
        return table_df




    @staticmethod
    def tem_save(table_df,table_time,sql_address='test.db'):
        # 定义保存按钮的函数：当点击保存时，连接数据库，将表格内容写入数据库
        table_df1 = Table.table_to_df(table_df,table_time)
        conn = sqlite3.connect(sql_address)
        # 注意路径格式
        table_df1.to_sql(table_time, conn, if_exists='replace')
        if not os.path.exists('./写实存档'):
            os.makedirs('./写实存档')
        try:
            table_df1.to_csv('./写实存档/{}.csv'.format(table_time))
        except PermissionError:
            remark_dialog = QDialog()
            QMessageBox.critical(remark_dialog, "注意", "请先关闭已打开的{}写实".format(table_time), QMessageBox.Ok | QMessageBox.Cancel,
                                 QMessageBox.Ok)
        #点按保存按钮时将写实存档为csv文件
        try:
            remote_conn = sqlite3.connect('remote.db')
            table_df1.to_sql(table_time, remote_conn, if_exists='replace')
            remote_conn.commit()
            remote_conn.close()
        except:
            print('{}analyse did not save into remote.db successfully'.format(table_time))
            pass
            # 存储一个名为 table_time + _analyse 的数据表到remote.db里， 用于远程分析使用
        import DataWash
        DataWash.check_if_overtime(table_df,table_time)


    @staticmethod
    def execute_eval():
        try:
            with open('./other/eval_word.txt','r') as word:
                exe_words = word.read()
                eval(exe_words)
        except:
            print(u'execute_eval函数出现错误')
            pass

class Remarks:
    def __init__(self):
        pass

    def show_dialog(self, remark_button, model,table_time,conn_name = 'test.db'):
        sql_name = table_time + ' breakdown'
        # 设数据库名称为：今日加breakdown 例如 "2020.12.22 breakdown"
        conn = sqlite3.connect(conn_name)
        cursor = conn.cursor()
        cursor.execute("select name from sqlite_master where type='table' order by name")
        table_list = cursor.fetchall()
        table_list = [j for i in table_list for j in i]
        if sql_name in table_list:
            df = pd.read_sql('select * from {}'.format('"' + sql_name + '"'), conn)
            df = df.iloc[:, 1:]
        else:
            df = pd.DataFrame(columns=['index', 'row_num', 'type', 'start_time', 'end_time'])
        conn.commit()
        conn.close()

        remark_dialog = QDialog()
        lay = QFormLayout(remark_dialog)
        edit1 = QComboBox()
        edit1.addItems(['取料机故障','皮带故障','混配卸船', '天气因素', '单线作业', '料粘', '其他'])
        edit2 = QLineEdit()
        edit2.setPlaceholderText('起始时间')
        edit4 = QLineEdit()
        edit4.setPlaceholderText('结束时间')
        edit3 = QTextEdit()
        button1 = QPushButton('确定添加')
        button2 = QPushButton('保存并退出')
        lay.addRow(edit1)#故障类型下拉菜单
        lay.addRow(edit2)#起始时间
        lay.addRow(edit4)#结束时间
        lay.addRow(edit3)#回显lineEdit
        lay.addRow(button1)
        lay.addRow(button2)

        x = remark_button.sender().geometry().x()
        y = remark_button.sender().geometry().y()
        pos = QtCore.QPoint(x, y)
        index_row = model.indexAt(pos).row()
        # index_row：所选的备注按钮的所在行数

        sql_df = df[df['row_num'] == index_row]
        sql_text = ''
        for index in range(len(sql_df)):
            single_list = sql_df.iloc[index].tolist()
            single_list_str = list(map(str, single_list))
            # ===single_list_str示例：['1', '4', '设备故障', '12']====
            single_list_str.insert(4, '至')
            single_text = ' '.join(single_list_str[2:]) + '\n'
            sql_text += single_text
        edit3.setText(sql_text)

        ###==========先回显既有的备注信息============================

        def content_show(df):
            #  LineEdit显示函数
            item_row, breakdown_type, breakdown_start_time, breakdown_end_time = index_row, edit1.currentText(), str(edit2.text()),str(edit4.text())
            if len(breakdown_start_time)== 0 or len(breakdown_end_time) == 0:
                QMessageBox.critical(remark_dialog,"注意", "请将起始时间和结束时间填写完整", QMessageBox.Ok | QMessageBox.Cancel,QMessageBox.Ok)
                # 若故障开始时间和结束时间任意一个没填，则不保存到Remark.df中，同时警告对话框
            else:
                df.loc[df.shape[0] + 1] = [df.shape[0] + 1, item_row, breakdown_type, breakdown_start_time,breakdown_end_time]
            # index:    ,item_row:索引（从0开始,控件所在的行数）， breakdown_type:故障类型 ， breakdown_time:故障时间
            sql_df = df[df['row_num'] == index_row]
            sql_text = ''
            for index in range(len(sql_df)):
                single_list = sql_df.iloc[index].tolist()
                single_list_str = list(map(str, single_list))
                # single_list_str示例：['1', '4', '设备故障', '12:30','13:00']
                if single_list_str[-1] == '':
                    continue
                # 如果single_list_str最后一个元素是空字符串，即故障时间未填写，则不在下方lineedit显示
                single_list_str.insert(4,'至')
                single_text = ' '.join(single_list_str[2:]) + '\n'
                # single_text 示例：'设备故障 111分钟'
                sql_text += single_text
            edit3.setText(sql_text)

        def content_save(df):
            if len(df) != 0:
                conn = sqlite3.connect('test.db')
                sql_name = table_time + ' breakdown'
                df.to_sql(sql_name, conn, if_exists='replace')
                conn.commit()
                conn.close()
            try:
                remote_conn = sqlite3.connect('remote.db')
                sql_name = table_time + ' breakdown'
                df.to_sql(sql_name, remote_conn, if_exists='replace')
                remote_conn.commit()
                remote_conn.close()
            except:
                pass
            remark_dialog.close()


        button1.clicked.connect(lambda: content_show(df))
        button2.clicked.connect(lambda: content_save(df))

        remark_dialog.exec_()


class MyVersionQTableWidget(QTableWidget):
    def __init__(self):
        super(MyVersionQTableWidget, self).__init__()

    def keyPressEvent(self, event):
        super(MyVersionQTableWidget, self).keyPressEvent(event)
        if event.key() == 16777220 or event.key() == 16777221:
            self.focusNextChild()


if __name__ == '__main__':
    pass