import pandas as pd
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QHeaderView,QLabel
from PyQt5.QtCore import Qt, QSize
# Create the main window
from UI import MyTable
from ManageFile import FileClass
from Data import DataClass
data = DataClass()
file = FileClass()
# خواندن داده‌ها از فایل csv و ذخیره آن‌ها در یک دیتافریم
data.read_display_data(file.display_data_path,file.current_file())
# ایجاد یک QTableWidget
print(file.display_list)
app = QApplication([])
table = QTableWidget()
table1 = MyTable()
table1.create_table(data.dp_df)
# تعیین تعداد سطرها و ستون‌های جدول به اندازه تعداد سطرها و ستون‌های دیتافریم
table.setRowCount(data.dp_df.shape[0])
table.setColumnCount(data.dp_df.shape[1])

# قرار دادن داده‌های دیتافریم در جدول
for i in range(data.dp_df.shape[0]):
    for j in range(data.dp_df.shape[1]):
        table_item = QTableWidgetItem(str(data.dp_df.iloc[i, j]))
        if j == 0 or i == 0 or j > 7: # For the first row and column, editing is disabled
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table.setItem(i, j, table_item)
# تعریف تابعی برای ذخیره تغییرات در دیتافریم و فایل csv
def save_data(row, col):
    if table.item(row, col) is None or table.item(row, col).text().strip() == '':
        QMessageBox.warning(None, "اخطار", "ستون خالی است!")
        return
    data.dp_df.iloc[row, col] = (table.item(row, col).text())
    data.write_display_data(file.display_data_path,file.current_file())
    autosize(table)
    print('Changes saved successfully!')

# تعریف signal برای ذخیره تغییرات هنگام ادیت کردن سلول
table.cellChanged.connect(save_data)

def autosize(table):
    for col in range(table.columnCount()):
        width = 0
        for row in range(table.rowCount()):
            item = table.item(row, col)
            if item is not None:
                width = max(width, table.fontMetrics().width(item.text()))
        if width > 0:
            table.setColumnWidth(col, width + 20)

def add_row(data,lst,table):
    data.dp_df.loc[len(data.dp_df.index)] = lst
    data.write_display_data(file.display_data_path,file.current_file())
    # ایجاد QTableWidget اگر قبلاً وجود نداشته باشد.
    if table.rowCount() == 0:
        table.setColumnCount(data.dp_df.shape[1])
        table.setHorizontalHeaderLabels(data.dp_df.columns.tolist())
    # اضافه کردن ردیف جدید به QTableWidget
    row_count = table.rowCount()
    table.insertRow(row_count)
    for j in range(len(data.dp_df.columns)):
        str1 = str(data.dp_df.iloc[row_count, j])
        table_item =QTableWidgetItem(str1)
        if j == 0 or j >7 or row_count == 1:
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table.setItem(row_count, j, table_item)
    table.scrollToItem(table.item(row_count, 0))
def remove_row():
    rows = set(index.row() for index in table.selectedIndexes())
    if not rows:
        QMessageBox.warning(None, "اخطار", "لطفاً یک یا چند سطر را انتخاب کنید!")
        return
    reply = QMessageBox.question(None, "حذف سطر", "آیا از حذف سطر(های) انتخاب شده مطمئن هستید؟", QMessageBox.Yes | QMessageBox.No)
    if reply == QMessageBox.Yes:
        for row in sorted(rows, reverse=True):
            table.removeRow(row)
            data.dp_df.drop(data.dp_df.index[row], inplace=True)
        data.dp_df.to_csv(rf'{file.display_data_path}\{file.current_file()}', encoding='utf-8-sig', index=False, header=None)
        autosize(table)
        print('Selected rows removed successfully!')

lst = ["دوشنبه-1407.43.12",178,
                  6512,
                   4366,
                   56,
                   547,
                  67,
                   954377,
            "اردی.40",
                   "F"]
# search_string = input ("search string: \n")
# result = df[df.iloc[:, 0].str.contains(search_string)]
# print (result)
def test(file,table1,str):
    table1.delete_table()
    if str == "N":
        df = pd.read_csv(rf'{file.display_data_path}\{file.get_next_file()}', encoding='utf-8-sig', header=None,
                         index_col=False)
    else :
        df = pd.read_csv(rf'{file.display_data_path}\{file.get_previous_file()}', encoding='utf-8-sig', header=None,
                         index_col=False)
    table1.create_table(df)
# تعریف دکمه‌های اضافه کردن سطر و حذف سطر
add_button = QPushButton('افزودن سطر')
next = QPushButton('Next')
previous = QPushButton('Previous')
previous.clicked.connect(lambda :test(file,table1,'P'))
next.clicked.connect(lambda :test(file,table1,"N"))
incrase_size_of_font = QPushButton('+')
decrease_size_of_font = QPushButton('-')
incrase_size_of_font.clicked.connect(lambda : table1.increase_font())
decrease_size_of_font.clicked.connect(lambda :table1.decrease_font())
widget = add_button.clicked.connect(lambda :add_row(data,lst,table))
remove_button = QPushButton('حذف سطر انتخاب شده')
remove_button.clicked.connect(remove_row)
# قرار دادن جدول و دکمه‌ها در ویجت
layout = QVBoxLayout()
layout_2 = QVBoxLayout()
layout_3 = QVBoxLayout()
layout_3.addWidget(table1.table)
main_layout= QVBoxLayout()
layout.addWidget(incrase_size_of_font)
layout.addWidget(next)
layout.addWidget(previous)
layout.addWidget(decrease_size_of_font)
layout.addWidget(table)
layout_2.addWidget(add_button)
layout_2.addWidget(remove_button)
widget = QWidget()
main_layout.addLayout(layout)
main_layout.addLayout(layout_2)
main_layout.addLayout(layout_3)
widget.setLayout(main_layout)
widget.setWindowTitle('جدول داده‌ها')
widget.showMaximized()

# تنظیم اندازه سلول‌ها بر اساس محتوا
autosize(table)
# اجرای برنامه
app.exec_()