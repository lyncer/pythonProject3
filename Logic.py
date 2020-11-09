import sys
from PyQt5.QtWidgets import *


class Table:
    def __init__(self):
        pass


    def table(self):
        model = QTableWidget()
        model.setRowCount(24)
        model.setColumnCount(15)
        model.setHorizontalHeaderLabels(['装车地点', '作业线路', '装车去向', '配空车次', '配空车数','实装重车','调妥时间',
                                         '封堵开始','封堵结束', '装车开始', '装车完毕','平车开始', '平车结束', '挂车时间', '备注'])

        table_layout = QHBoxLayout()
        table_layout.addWidget(model)
        # 设置装车地点的列表头
        # 表格中添加控件
        # 先定义一个生成combox的函数 每次生成一个combox新对象
        def reborn_combox():
            combox = QComboBox()
            combox.addItem('专一')
            combox.addItem('专二')
            return combox
        for num in range(8):
            model.setItem(num,0,QTableWidgetItem('实业一期'))
            model.setCellWidget(num, 1, reborn_combox())

        def reborn_combox1():
            combox = QComboBox()
            combox.addItem('专三')
            combox.addItem('专四')
            return combox
        for num in range(8,14):
            model.setCellWidget(num,1,reborn_combox1())
            model.setItem(num,0,QTableWidgetItem('实业二期'))
        def reborn_combox2():
            combox = QComboBox()
            combox.addItem('矿一')
            combox.addItem('矿二')
            return combox
        for num in range(14,24):
            model.setItem(num,0,QTableWidgetItem('矿三'))
            model.setCellWidget(num,1,reborn_combox2())

        # 定义装车去向的函数
        def reborn_combox3():
            quxiang_list = '无 古冶国义 首钢沙河驿 鑫达沙河驿 九江沙河驿 荣信沙河驿 松汀沙河驿 东华胥各庄 ' \
                           '瑞丰胥各庄 燕钢迁安 津西贾庵子 唐山东海雷庄 古冶经安 河北东海古冶 河北东海雷庄 河钢唐南 港陆团瓢庄'.split()
            combox = QComboBox()
            for name in quxiang_list:
                combox.addItem(name)
            return combox
        for num in range(24):
            model.setCellWidget(num,2,reborn_combox3())

        print(model.cellWidget(0,1).currentText())

        return table_layout