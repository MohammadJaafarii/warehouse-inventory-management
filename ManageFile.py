import os
import datetime
class File:
    def __init__(self):
        if not os.path.exists("information"):
            os.makedirs("information")
        self.information_path = self.get_path()
        self.getting_the_names_of_all_files(self.information_path)
        self.dir_list = []
        self.getting_the_names_of_all_files(self.information_path)
        self.sort_files_according_to_Date()
        self.index_of_current_file = len(self.dir_list) - 1
    def current_file(self):
        if self.index_of_current_file != -1:
            return self.dir_list[self.index_of_current_file]
    def file_is_exist(self,path):
        if os.path.isfile(path):
            return True
        else:
            return False
    def getting_the_names_of_all_files(self , path):
        self.dir_list = os.listdir(path)
    def get_path(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'information')
        return data_dir
    def next_file(self):
        if self.index_of_current_file == -1:
            #show suitable message
            return False
        elif self.index_of_current_file == len(self.dir_list) - 1 :
            self.index_of_current_file = 0
        else:
            self.index_of_current_file += 1
        return self.dir_list[self.index_of_current_file]
    def sort_files_according_to_Date(self):
        self.dir_list = sorted(self.dir_list, key=lambda x: os.path.getmtime(os.path.join(self.information_path, x)))

        for file in self.dir_list:
            file_path = os.path.join(self.information_path, file)
            mod_time = os.path.getmtime(file_path)
            mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{file} was last modified on {mod_time_str}")
