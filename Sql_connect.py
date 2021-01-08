import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from datetime import datetime
import dataset
import pandas as pd
import sqlite3
from PyQt5 import QtCore


class Sql:
    def __init__(self):
        pass


    @staticmethod
    def try_connect_sql(table_model):
        if QSqlDatabase.contains("qt_sql_default_connection"):
            database = QSqlDatabase.database("qt_sql_default_connection")
        else:
            database = QSqlDatabase.addDatabase('QSQLITE')
            database.setDatabaseName('test.db')
        if not database.open():
            QMessageBox.critical(table_model,'警告','数据库链接异常',QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
        return database


