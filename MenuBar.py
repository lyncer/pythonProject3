from PyQt5.QtWidgets import *
from datetime import datetime,timedelta
import Logic
import sqlite3
import os
from dateutil.parser import parse


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
            with open('other/quxiang.txt', 'a', encoding='utf-8') as quxiang:
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

            button1.clicked.connect(
                lambda: Logic.Table.read_table(table_model, edit1.currentText(), status_bar, sql_address=dataset_address,Groupbox=GroupBox))
            button2.clicked.connect(dialog_close)
            remote_tables_dialog.exec_()

    #=================导出函数================
    @staticmethod
    def experted_excel_to_shared_folder(table_model,table_time,status_bar):
        def openFile(table_model):
            if not os.path.exists("./表格"):
                os.makedirs("./表格")
            get_directory_path = QFileDialog.getExistingDirectory(table_model,
                                                                  "选取指定文件夹",
                                                                  "./表格")
            save_path = str(get_directory_path)
            return save_path # 默认路径是 D:\\sql\表格

        import DataWash
        final_df = DataWash.table_analyse(table_model,table_time)
        # ==================调整各个时间列的格式从 ‘xxxx-xx-xx xx:xx’ 至 ‘xx：xx’
        time_col_list = ['调妥时间', '封堵开始', '封堵结束', '装车开始', '装车完毕', '平车开始', '平车结束', '具备挂车条件', '挂车时间']
        time_caculate_col_list = ['线内用时','待挂用时']
        for time_col_name in time_col_list:
            final_df[time_col_name] = final_df[time_col_name].fillna('')
            final_df[time_col_name] = final_df[time_col_name].astype('str')
            final_df[time_col_name] = '{} '.format(table_time) + final_df[time_col_name]
            final_df[time_col_name] = final_df[time_col_name].replace('{} '.format(table_time), '')
            for i, v in final_df[time_col_name].items():
                try:
                    time_time = parse(v)
                    time_str = datetime.strftime(time_time, '%H:%M')
                    final_df.loc[i, time_col_name] = time_str
                except:
                    pass

        def time_trans(hours:float): # hours是4.5这样的浮点数
            if not hours == 0:
                float_time = hours  # in minutes
                hours, seconds = divmod(float_time * 3600, 3600)  # split to hours and seconds
                minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                hours,minutes,seconds = list(map(int,[hours,minutes,seconds]))
                return '{}小时{}分钟'.format(hours,minutes)
        for time_col_name in time_caculate_col_list:
            final_df[time_col_name] = final_df[time_col_name].apply(time_trans)


        file_save_path = openFile(table_model) + '/{}.xlsx'.format(table_time)
        try:
            final_df.to_excel(file_save_path)
            print('success to save {}.xlsx into "biaoge" dictionary'.format(table_time))
        except PermissionError:
            remark_dialog = QDialog()
            QMessageBox.critical(remark_dialog, "注意", "请先关闭已打开的分析表", QMessageBox.Ok | QMessageBox.Cancel,
                                 QMessageBox.Ok)


