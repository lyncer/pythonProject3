import sqlite3
import os
import cx_Oracle
import pandas as pd
import time
from datetime import datetime


class tsz:
    def __init__(self,name = 'tsz',password = 'tsz',address = '10.68.2.165:1521/oraqcp'):
        self.con = cx_Oracle.connect(name,password,address)
        self.cursor = self.con.cursor()

    # 获取表名的函数
    def get_file_name(self,path='/Users/lvgaofeng/Desktop/table_new'):
        filename_list = os.listdir(path)
        excel_name_list = [table_name for _ in filename_list for table_name in os.path.splitext(_)][::2]
        return excel_name_list

    def get_sql_name(self):
        pass

    def down_load(self,sql_name,*args):
        save_path = '/Users/lvgaofeng/Desktop/table_new/{}.csv'

        print(sql_name)
        for name in sql_name:
            try:
                df = pd.read_sql('select * from {}'.format('"' + name + '"'), self.con)
                df1 = df[df['FZM']=='曹妃甸南']
                df1.to_csv(save_path.format(name))
            except:
                print(name)
                pass



col_dict = {'CH':'车号','CZ':'车型','DZM':'到站名','FZM':'发站名','SHR':'收货人',
            'YDH':'运单号','DDCC':'到达车次','HPH':'货票号','DDRQ':'到达日期','HPHYSJ':'货票**时间',
            'SWH':'顺位号','GDM':['K1','K2','Z1','Z2','Z3','Z4']}


condition = (df['GDM'] in col_dict['GDM']) and (df['DFRQ'] > datetime(2021,1,31))

path = '/Users/lvgaofeng/Desktop/table_new'
os.chdir(path)
for name in os.listdir(path):
    try:
        df = pd.read_csv(name)
        df1 = df[df['CID']=='VXP2021012600364874703']
        print(df1,'\n',name,'='*44)
    except:
        pass

