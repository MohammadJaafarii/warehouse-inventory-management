from pandas import DataFrame
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QHeaderView
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QHeaderView,QFontComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
class MyTable:
    def __init__(self):
        self.table = QTableWidget()
        self.font = 12
    def create_table(self,df):
        #number of rows and columns for putting data from data frame in table
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        font = QFont('Arial', self.font)
        self.table.setFont(font)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                table_item = QTableWidgetItem(str(df.iloc[i, j]))
                table_item.setTextAlignment(Qt.AlignCenter)
                table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(i, j, table_item)
                self.autosize()
    def add_row(self, df,lst):
        df.loc[len(df.index)] = lst
        df.to_csv('1402.4.csv', encoding='utf-8-sig', index=False, header=None)
        # ایجاد QTableWidget اگر قبلاً وجود نداشته باشد.
        if self.table.rowCount() == 0:
            self.table.setColumnCount(df.shape[1])
            self.table.setHorizontalHeaderLabels(df.columns.tolist())
        # اضافه کردن ردیف جدید به QTableWidget
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        for j in range(len(df.columns)):
            str1 = str(df.iloc[row_count, j])
            table_item = QTableWidgetItem(str1)
            table_item.setTextAlignment(Qt.AlignCenter)
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row_count, j, table_item)
        self.table.scrollToItem(self.table.item(row_count, 0))
        self.autosize()
    def autosize(self):
        for col in range(self.table.columnCount()):
            width = 0
            for row in range(self.table.rowCount()):
                item = self.table.item(row, col)
                if item is not None:
                    width = max(width, self.table.fontMetrics().width(item.text()))
            if width > 0:
                self.table.setColumnWidth(col, width + 20)
    def increase_font(self):
        self.font += 1
        font = QFont('Arial', self.font)
        self.table.setFont(font)
        self.autosize()
    def decrease_font(self):
        if self.font >0 :
            self.font -= 1
            font = QFont('Arial', self.font)
            self.table.setFont(font)
            self.autosize()
    def delete_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
class AddButton:
    def __init__(self):
        self.addbutton = QPushButton("افزودن")
        self.addbutton.clicked.connect(lambda:self.create_form_for_getting_info())
    def create_form_for_getting_info(self):
        pass
