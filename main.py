import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QHeaderView,QLabel
from PyQt5.QtCore import Qt, QSize
# Create the main window
from UI import MyTable
from ManageFile import File
file = File()
# خواندن داده‌ها از فایل csv و ذخیره آن‌ها در یک دیتافریم
df = pd.read_csv(rf'{file.information_path}\{file.current_file()}', encoding='utf-8-sig', header=None, index_col=False)
print (df.shape[0],df.shape[1])
# ایجاد یک QTableWidget
print(file.dir_list)
app = QApplication([])
table = QTableWidget()
table1 = MyTable()
table1.create_table(df)
# تعیین تعداد سطرها و ستون‌های جدول به اندازه تعداد سطرها و ستون‌های دیتافریم
table.setRowCount(df.shape[0])
table.setColumnCount(df.shape[1])

# قرار دادن داده‌های دیتافریم در جدول
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        table_item = QTableWidgetItem(str(df.iloc[i, j]))
        if j == 0 or i == 0 or j > 7: # For the first row and column, editing is disabled
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table.setItem(i, j, table_item)

# تعریف تابعی برای ذخیره تغییرات در دیتافریم و فایل csv
def save_data(row, col):
    if table.item(row, col) is None or table.item(row, col).text().strip() == '':
        QMessageBox.warning(None, "اخطار", "ستون خالی است!")
        return
    df.iloc[row, col] = (table.item(row, col).text())
    df.to_csv(rf'{file.information_path}\{file.current_file()}', encoding='utf-8-sig', index=False, header=None)
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

def add_row(df,lst,table):

    df.loc[len(df.index)] = lst
    df.to_csv(rf'{file.information_path}\{file.current_file()}', encoding='utf-8-sig', index=False, header=None)
    # ایجاد QTableWidget اگر قبلاً وجود نداشته باشد.
    if table.rowCount() == 0:
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns.tolist())
    # اضافه کردن ردیف جدید به QTableWidget
    row_count = table.rowCount()
    table.insertRow(row_count)
    for j in range(len(df.columns)):
        str1 = str(df.iloc[row_count, j])
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
            df.drop(df.index[row], inplace=True)
        df.to_csv(rf'{file.information_path}\{file.current_file()}', encoding='utf-8-sig', index=False, header=None)
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

# تعریف دکمه‌های اضافه کردن سطر و حذف سطر
add_button = QPushButton('افزودن سطر')
incrase_size_of_font = QPushButton('+')
decrease_size_of_font = QPushButton('-')
incrase_size_of_font.clicked.connect(lambda : table1.increase_font())
decrease_size_of_font.clicked.connect(lambda :table1.decrease_font())
widget = add_button.clicked.connect(lambda :add_row(df,lst,table))
remove_button = QPushButton('حذف سطر انتخاب شده')
remove_button.clicked.connect(remove_row)
# قرار دادن جدول و دکمه‌ها در ویجت
layout = QVBoxLayout()
layout_2 = QVBoxLayout()
layout_3 = QVBoxLayout()
layout_3.addWidget(table1.table)
main_layout= QVBoxLayout()
layout.addWidget(incrase_size_of_font)
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