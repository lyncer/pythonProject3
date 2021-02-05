# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from Logic import Table,Remarks,MyVersionQTableWidget
from PyQt5.QtWidgets import *
from datetime import datetime,timedelta
from MenuBar import Menubar
import sqlite3
import DataWash

Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数', '实装重车', '调妥时间',
              '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件','挂车时间', '线内作业时间分析','待挂时间分析']

with open('./other/quxiang.txt','r',encoding='utf-8') as quxiang:
    quxiang_list = quxiang.read().split(',')
    quxiang_list = [quxiang_name.strip() for quxiang_name in quxiang_list ]


Today = datetime.today()
# 定义today 为“2020.xx.xx”格式的字符串
today =  Today.strftime('%Y.%m.%d')
tomorrow = Today + timedelta(days=1)
tomorrow = tomorrow.strftime('%Y.%m.%d')



class Ui_MainWindow(object):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(Main_Window)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("曹妃甸南货调写实系统")
        MainWindow.resize(1424, 938)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 228, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.report_model = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.report_model.setObjectName("report_model")
        self.horizontalLayout.addWidget(self.report_model)
        self.input_model = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.input_model.setObjectName("input_model")
        self.horizontalLayout.addWidget(self.input_model)
        self.save_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.input_model.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 85, 1821, 801))
        self.tableView.setObjectName("tableView")
        self.GroupBox = QtWidgets.QComboBox(self.centralwidget)
        self.GroupBox.setGeometry(QtCore.QRect(840, 10, 121, 26))
        self.GroupBox.setObjectName("GroupBox")
        self.GroupBox.addItem("")
        self.GroupBox.addItem("")
        self.GroupBox.addItem("")
        self.GroupBox.addItem("")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(660, 0, 163, 93))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.StartTime = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget)
        self.StartTime.setObjectName("StartTime")
        self.verticalLayout.addWidget(self.StartTime)
        self.EndTime = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget)
        self.EndTime.setObjectName("EndTime")
        self.verticalLayout.addWidget(self.EndTime)
        self.AggBox = QtWidgets.QComboBox(self.centralwidget)
        self.AggBox.setGeometry(QtCore.QRect(840, 50, 121, 26))
        self.AggBox.setObjectName("AggBox")
        self.AggBox.addItem("")
        self.AggBox.addItem("")
        self.AggBox.addItem("")
        self.AggBox.addItem("")
        self.over_time = QtWidgets.QCheckBox(self.centralwidget)
        self.over_time.setGeometry(QtCore.QRect(560, 10, 71, 31))
        self.over_time.setObjectName("over_time")
        self.output_line = QtWidgets.QLineEdit(self.centralwidget)
        self.output_line.setGeometry(QtCore.QRect(230, 10, 321, 31))
        self.output_line.setObjectName("output_line")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.model = MyVersionQTableWidget()
        self.model.setInputMethodHints(Qt.ImhHiddenText)
        self.model.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # tablewidget自适应行高
        # self.model.horizontalHeader().setSectionResizeMode(1)
        # self.model.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))

        self.model.setRowCount(26)
        self.model.setColumnCount(17)
        self.model.setHorizontalHeaderLabels(Head_label)


        # 引入菜单栏
        self.bar = MainWindow.menuBar()
        self.file = self.bar.addMenu('文件')
        self.save = QAction('过表', MainWindow)
        self.file.addAction(self.save)

        self.edit = self.bar.addMenu('编辑')
        add_station = QAction('添加到站',MainWindow)
        remote_table_from_huodiao = QAction('远程读表',MainWindow)
        self.edit.addAction(add_station)
        self.edit.addAction(remote_table_from_huodiao)

        self.experted = self.bar.addMenu('导出')
        expertd = QAction('导出为excel',MainWindow)
        self.experted.addAction(expertd)

        self.view = self.bar.addMenu('视图')
        self.report_docx = QAction('生成写实word', MainWindow)
        self.view.addAction(self.report_docx)
        self.report_docx.triggered.connect(lambda :DataWash.Report_docx(self.model,self.GroupBox.currentText()).wash_use_table())
        self.save.triggered.connect(lambda :self.passtable(self.statusbar,self.model))
        self.input_model.clicked.connect(Table.execute_eval)
        self.report_model.clicked.connect(lambda :DataWash.check_if_overtime(self.model,self.GroupBox.currentText()))



        def reborn_combox():
            # 先定义一个生成combox的函数 每次生成一个combox新对象
            combox = QComboBox()
            combox.addItem('专一')
            combox.addItem('专二')
            return combox
        def reborn_combox1():
            combox = QComboBox()
            combox.addItem('专三')
            combox.addItem('专四')
            return combox
        def reborn_combox2():
            combox = QComboBox()
            combox.addItem('矿一')
            combox.addItem('矿二')
            return combox
        # 定义装车去向的函数
        def reborn_combox3():
            combox = QComboBox()
            for name in quxiang_list:
                combox.addItem(name)
            return combox
        for num in range(8):
            self.model.setItem(num, 0, QTableWidgetItem('实业一期'))
            self.model.setCellWidget(num, 1, reborn_combox())
        for num in range(8, 17):
            self.model.setCellWidget(num, 1, reborn_combox1())
            self.model.setItem(num, 0, QTableWidgetItem('实业二期'))
            print(self.model.item(num,0))
        for num in range(17, 26):
            self.model.setItem(num, 0, QTableWidgetItem('矿三'))
            self.model.setCellWidget(num, 1, reborn_combox2())
        for num in range(26):
            self.model.setCellWidget(num, 2, reborn_combox3())

        def bulid_remark_button():
            count = -1
            def inner_bulid_remark_button():
                nonlocal count
                count += 1
                self.remark_button = QPushButton('添加备注')
                self.remark_button.setObjectName(str(count))
                print(self.remark_button.objectName())
                self.remark_button.clicked.connect(lambda :Remarks.show_dialog(self.remark_button,self.remark_button,self.model,self.GroupBox.currentText()))
                return self.remark_button
            return inner_bulid_remark_button
        Bulid_remark_button = bulid_remark_button()
        for num in range(0,26):
            self.model.setCellWidget(num, 17, Bulid_remark_button()) #设置备注按钮的位置 第17列（隐藏列）
        # =============数据库内列表加入多选栏=======================
        def table_list_for_combox(test_all_tables=Table.test_all_tables, time_format='%Y.%m.%d'):
            table_name_list = []
            for table_name in test_all_tables:
                try:
                    table_name = datetime.strptime(table_name, time_format)
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
            return ls[-1], ls[-2], ls[-3], ls[-4]
            # table_name_list 为符合datetime格式的数据表名字
        self.one , self.two , self.three , self.four = table_list_for_combox()
            # =======================================================


        # 将table函数返回的layout置于tableview控件之中
        self.table_layout = QHBoxLayout()
        self.table_layout.addWidget(self.model)
        self.tableView.setLayout(self.table_layout)
        Table.read_table(self.model,self.two,self.statusbar)
        # 程序打开时，自动反写GroupBox当前时间的数据表
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # 信号——槽函数
        self.save_button.clicked.connect(lambda :Table.tem_save(self.model,self.GroupBox.currentText()))
        add_station.triggered.connect(lambda :Menubar.addStation(MainWindow,MainWindow))
        expertd.triggered.connect(lambda :Menubar.experted_excel_to_shared_folder(self.model,self.GroupBox.currentText(),self.statusbar))
        remote_table_from_huodiao.triggered.connect(lambda :Menubar.Win_Remote_table_from_huodiao(MainWindow,MainWindow,self.model,self.statusbar,self.GroupBox))
        self.GroupBox.currentIndexChanged.connect(self.groupchange)
        Table.init_sql(self)

            # ================组合下拉框改变函数==========================================================
    def groupchange(self):
        Table.read_table(self.model,self.GroupBox.currentText(),self.statusbar)
        print(self.GroupBox.currentText())

            # ================过表函数==========================================================
    def passtable(self, status_bar, table_model):
        button = QMessageBox.critical(table_model, "注意", "今日写实填写完毕后方可过表操作，确定过表吗？",
                                      QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Ok:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("select name from sqlite_master where type='table' order by name")
            test_all_tables = cursor.fetchall()
            # 打印出test.db中所有表名
            # cursor.fetchall()输出的格式为：[('2020.12.11',), ('2020.12.12',), ('2020.12.14',)]
            test_all_tables = [j for i in test_all_tables for j in
                               i]  # 格式为：['2020.12.11', '2020.12.12', '2020.12.14']
            if tomorrow not in test_all_tables:
            # 如果数据库里没有名为today的表
                status_bar.showMessage('成功过表，目前写实日期为' + tomorrow)
                sentence = "CREATE TABLE " + "'" + tomorrow + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT," \
                                                                    "'装车去向' TEXT,'配空车次' TEXT," \
                                                                    "'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT," \
                                                                    "'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' " \
                                                                    "TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT," \
                                                                    "'挂车时间' TEXT,'备注' TEXT," \
                                                                    "PRIMARY KEY('id' AUTOINCREMENT));"
                cursor.execute(sentence)
                button = QMessageBox.critical(table_model, "注意", "过表成功，请重新启动程序！",
                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            else:
                status_bar.showMessage('已存在{}数据表'.format(tomorrow))
                Table.read_table(table_model, table_time=tomorrow, status_bar=self.statusbar)
                self.GroupBox.setCurrentText(tomorrow)
                # todo 若保存也是保存到tomorrow才行
            conn.commit()
            conn.close()


    #================================================================================================
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "曹妃甸南货调写实系统"))
        self.report_model.setText(_translate("MainWindow", "报表模式"))
        self.input_model.setText(_translate("MainWindow", "输入模式"))
        self.save_button.setText(_translate('MainWindow', '保存'))
        self.GroupBox.setItemText(0, _translate("MainWindow", self.one))
        self.GroupBox.setItemText(1, _translate("MainWindow", self.two))
        self.GroupBox.setItemText(2, _translate("MainWindow", self.three))
        self.GroupBox.setItemText(3, _translate("MainWindow", self.four))
        self.AggBox.setItemText(0, _translate("MainWindow", "无"))
        self.AggBox.setItemText(1, _translate("MainWindow", "用时总和"))
        self.AggBox.setItemText(2, _translate("MainWindow", "用时平均值"))
        self.AggBox.setItemText(3, _translate("MainWindow", "用时极值"))
        self.over_time.setText(_translate("MainWindow", "超时"))
        self.GroupBox.setCurrentIndex(1)





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    Main_Window = QtWidgets.QMainWindow()
    Ui = Ui_MainWindow()
    Ui.setupUi(Main_Window)
    Main_Window.show()
    sys.exit(app.exec_())
