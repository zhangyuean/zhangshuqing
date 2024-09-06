import subprocess
import os

class CheckFile:
    def __init__(self, file_path, dir_path, file_name):
        self.path = file_path
        self.dir_path = dir_path
        self.file_name = file_name

    def search_file(self):
        results = []
        target_file = self.file_name
        for dirpath, dirnames, filenames in os.walk(self.dir_path):
            for filename in filenames:
                if target_file in str(filename):
                    print(f'驱动包中找到文件{filename}')
                    results.append(os.path.join(dirpath, filename))
        return results

    def check_cat_sigature(self):
        cmd = f'certutil -dump {self.path}'
        out = subprocess.check_output(cmd, text=True, errors='ignore')
        line = out.splitlines()
        n = 0
        for i in line:
            if 'Quectel' in i:
                print(f'检查到cat文件{self.path}中存在敏感词:{i}')
                n += 1
        if not n:
            return True
        else:
            return False