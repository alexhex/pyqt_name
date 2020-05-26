# -*- coding: utf-8 -*-

import sqlite3
import csv
# import xlwings as xw
import os


folderpath = os.path.dirname(os.path.abspath(__file__))
excel_file = 'foreign_name_list_1.csv' 
excel_file_path  = os.path.join(folderpath, excel_file)
excel_file_2 = 'foreign_name_list_2.csv' 
excel_file_path_2  = os.path.join(folderpath, excel_file)

    

# table_1 = sht_1.range('B2:D383740').value
# print (table_1)
sqlite_file = 'foreign_name_list.sqlite' #数据库文件名称
sqlite_file_path = os.path.join(folderpath, sqlite_file)

table_name = 'foreign_name_table' #要创建的表格的名称

# 连接到数据库文件
conn = sqlite3.connect(sqlite_file_path)
c = conn.cursor()

# 创建表
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
.format(tn=table_name, nf='ID', ft='INTEGER'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
.format(tn=table_name, cn="original", ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
.format(tn=table_name, cn="nation", ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
.format(tn=table_name, cn="trans", ct='TEXT'))

with open(excel_file_path, 'r', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    to_db = [(row['ID'], row['original'], row['nation'], row['trans'])\
    for row in dr]

c.executemany("INSERT INTO 'foreign_name_table' (ID, original, nation, trans)\
    VALUES (?, ?, ?, ?);", to_db)

with open(excel_file_path_2, 'r', encoding='utf-8-sig') as fin:
    dr = csv.DictReader(fin)
    to_db = [(row['ID'], row['original'], row['nation'], row['trans'])\
    for row in dr]

c.executemany("INSERT INTO 'foreign_name_table' (ID, original, nation, trans)\
    VALUES (?, ?, ?, ?);", to_db)



conn.commit()
conn.close()

# for i in range(2,383742):
# # for i in range(2,2069):
#     vals = sht_1.range('A'+str(i)+':'+'D'+str(i)).value
#     if i%100 == 0:
#         print (vals)
#     foreign_name = sht_1.range('B'+str(i)).value
#     if foreign_name:
#         try:
#             c.execute("INSERT INTO foreign_name_table (ID, original, nation, trans) VALUES (?, ?, ?, ?)",\
#            (vals))
#         except sqlite3.IntegrityError:
#             print('ERROR: ID already exists in PRIMARY KEY column {}'.format("ID"))


# for i in range(2,293136):
# # for i in range(2,10):
#     vals = sht_2.range('A'+str(i)+':'+'D'+str(i)).value
#     foreign_name = sht_2.range('B'+str(i)).value
#     if i%100 == 0:
#         print (vals)
#     if foreign_name:
#         try:
#             c.execute("INSERT INTO foreign_name_table (ID, original, nation, trans) VALUES (?, ?, ?, ?)",\
#            (vals))
#         except sqlite3.IntegrityError:
#             print('ERROR: ID already exists in PRIMARY KEY column {}'.format("ID"))

 
    # print (vals)
    # c.execute()
# for row in c.execute("SELECT original, trans FROM foreign_name_table"):
    # print(row)
