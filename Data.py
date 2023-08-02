import pandas as pd
from PyQt5.QtWidgets import QMessageBox , QDesktopWidget
from PyQt5.QtGui import QFont
class DataClass:
    def read_display_data(self,display_path,filename):
        self.dp_df = pd.read_csv(rf'{display_path}\{filename}', encoding='utf-8-sig', header=None,index_col=False)
    def write_display_data(self,display_path,filename):
        self.dp_df.to_csv(rf'{display_path}\{filename}', encoding='utf-8-sig', index=False, header=None)
    def read_pure_data(self,pure_path,filename):
        self.pr_df = pd.read_csv(rf'{pure_path}\{filename}', encoding='utf-8-sig', header=None,index_col=False)
    def write_pure_data(self,pure_path,filename):
        self.pr_df.to_csv(rf'{pure_path}\{filename}', encoding='utf-8-sig', index=False, header=None)
    def add_row_to_dataframe(self,lst):
        try:
            self.dp_df.loc[len(self.dp_df.index)] = lst
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("مشکلی پیش آمده است!")
            msg.setFont(QFont("Arial", 12))
            msg_rect = msg.frameGeometry()
            screen_center = QDesktopWidget().availableGeometry().center()
            msg_rect.moveCenter(screen_center)
            msg.move(msg_rect.topLeft())
            msg.exec_()









