# 从生成的.py文件导入定义的窗口类
import ui_mainwindow
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtGui, QtWidgets, QtCore
import sys, os, sqlite3

###########################################
folderpath = os.path.dirname(os.path.abspath(__file__))
sqlite_file = 'foreign_name_list.sqlite' 
sqlite_file_path = os.path.join(folderpath, sqlite_file)
table_name = 'foreign_name_table' 
###########################################

# 定义数据模型
###########################################
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header


    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
                             key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))
###########################################

# 定义主窗体
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
    
########################################
        self.ui.search_btn.clicked.connect(self.search)
        self.init_db()
        # self.tablemodel = table_model
########################################
    
########################################
    def search(self):

        columnheader = ['Name', 'Nation', 'Trans']
        txt = self.ui.lineEdit.text()
        print (txt)
        results = self.c.execute("SELECT * FROM {tn} WHERE original LIKE '{nm}%' limit 100"\
        .format(tn = table_name, nm = txt))
        result_list = []
        for row in results:
            result_list.append(row[1:])
        tablemodel = MyTableModel(self, result_list, columnheader) 

        # print (result_list)
        self.ui.tableView.setModel(tablemodel)


    def init_db(self):
        self.conn = sqlite3.connect(sqlite_file_path)
        self.c = self.conn.cursor()
########################################



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # a_blank_tm = MyTableModel()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())