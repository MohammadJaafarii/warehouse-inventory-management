import os
import datetime
class File:
    def __init__(self):
        self.create_folders()
        self.display_list = []
        self.getting_the_names_of_all_files(self.display_data_path)
        self.sort_files_according_to_Date()
        self.index_of_current_file = len(self.display_list) - 1
    def create_folders (self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.Database_path = os.path.join(base_dir, "Database")

        if not os.path.exists(self.Database_path):
            os.makedirs(self.Database_path)
        self.pure_data_path = os.path.join(self.Database_path, "Pure Data")
        if not os.path.exists(self.pure_data_path):
           os.makedirs(self.pure_data_path)
        self.display_data_path = os.path.join(self.Database_path, "Display Data")
        if not os.path.exists(self.display_data_path):
            os.makedirs(self.display_data_path)
    def current_file(self):
        if self.index_of_current_file < 0 :
            print("Error")
        else:
            return self.display_list[self.index_of_current_file]

    def file_is_exist(self,path):
        if os.path.isfile(path):
            return True
        else:
            return False
    def getting_the_names_of_all_files(self , path):
        self.display_list = os.listdir(path)
    def get_path(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'information')
        return data_dir
    def get_next_file(self):
        if self.index_of_current_file == -1:
            #show suitable message
            return False
        elif self.index_of_current_file == len(self.display_list) - 1 :
            self.index_of_current_file = 0
        else:
            self.index_of_current_file += 1
        return self.display_list[self.index_of_current_file]
    def get_previous_file(self):
        if self.index_of_current_file == -1 :
            return False
        elif self.index_of_current_file == 0:
            self.index_of_current_file = len(self.display_list) - 1
        else:
            self.index_of_current_file -= 1
        return self.display_list[self.index_of_current_file]
    def sort_files_according_to_Date(self):
        self.display_list = sorted(self.display_list, key=lambda x: os.path.getmtime(os.path.join(self.display_data_path, x)))
