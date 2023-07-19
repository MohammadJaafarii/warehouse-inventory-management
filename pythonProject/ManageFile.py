import os
class File:
    def file_is_exist(self,path):
        if os.path.isfile(path):
            return True
        else:
            return False
