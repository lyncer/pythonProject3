import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQuery
from datetime import datetime
import dataset

Head_label = ['装车地点', '作业线路', '装车去向', '配空车次', '配空车数','实装重车','调妥时间',
                                         '封堵开始','封堵结束', '装车开始', '装车完毕','平车开始', '平车结束', '挂车时间', '备注']


today = datetime.today()
# 定义today 为“2020.xx.xx”格式的字符串
today = '.'.join(map(str, [today.year, today.month, today.day]))



class Table:
    def __init__(self):
        pass

    def init_sql(self):
        # 初始化数据库

        # db = dataset.connect('sqlite:///test.db')
        # print(db.tables)
        # cursor = db.query("SELECT * FROM '2020.12.1';")
        # print([i for i in cursor.result_proxy])
        # data = dict(装车地点='I am a aaabanana!')
        # data = dict(zip(('as','sf'),(23,55)))
        database = QSqlDatabase.addDatabase('QSQLITE')
        database.setDatabaseName('test.db')
        if not database.open():
            print('数据库建立失败')
        else:
            query = QSqlQuery()
            # 若数据库中已经存在名为today的数据表则将其删除，并打印"成功删除"
            if today in database.tables():
                sentence = "DROP TABLE" + " " + "'" + today + "'"
                print(sentence)
                query.exec_(sentence)
                print('成功删除表 {}'.format(today))
                print(database.tables())
            # 将today设为数据表的名字,建立完整的数据表
            sentence = "CREATE TABLE " + "'" + today + "'" + " ('id' INTEGER,'装车地点' TEXT, '作业线路' TEXT,'装车去向' TEXT,'配空车次' TEXT,'配空车数' TEXT,'实装重车' TEXT,'调妥时间' TEXT,'封堵开始' TEXT,'封堵结束' TEXT,'装车开始' TEXT,'装车完毕' TEXT,'平车开始' TEXT,'平车结束' TEXT,'挂车时间' TEXT,'备注' TEXT,PRIMARY KEY('id' AUTOINCREMENT));"
            query.exec_(sentence)
            print('成功建立表格 {}'.format(today))
            print('当前表格列表：',database.tables())
            database.close()



    #点击保存按钮，将数据更新至数据库

    @staticmethod
    def save_table(table_model):
        pass









