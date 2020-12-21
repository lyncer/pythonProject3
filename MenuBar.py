from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from datetime import datetime
from PyQt5.QtGui import *




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