import time
import os
from datetime import datetime
from functools import reduce
import re
import chardet
import win32api
import shutil

class delete:

    def traverse_files(path):
        results = []
        file = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                results.append(os.path.join(dirpath, filename))
        for i in results:
            a = i.split('\\')
            b = '\\'.join(a[:6])
            file.append(b)

        file = list(set(file))
        return file

    def get_file_date(path):
        ctime = os.path.getctime(path)
        ctime_string = datetime.fromtimestamp((int(ctime)))
        return ctime_string

    def delete_file(path):
        try:
            shutil.rmtree(path)
        except Exception:
            os.remove(path)

    def change_path(x, y):
        return x + '\\' + y


def traverse_files(driver_path, target_file = ''):
    results = []
    for dirpath, dirnames, filenames in os.walk(driver_path):
        for filename in filenames:
            if target_file in str(filename):
                print(f'{driver_path}路径下找到文件{filename}')
                results.append(os.path.join(dirpath, filename))
            elif target_file == '':
                print(f'{driver_path}路径下找到文件{filename}')
                results.append(os.path.join(dirpath, filename))
    if results == []:
        print(f'{driver_path}文件夹内未找到包含{target_file}的文件，请检查')
    return results

def test_hlk_logo(file_path):
    cmd = '.\\sigcheck64.exe -d ' + file_path + ' | findstr OS:'
    print("cmd: {}".format(cmd))
    with os.popen(cmd) as f:
        content = f.read()
        print(content)
    return content

# 定义获取文件解码方式方法
def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


# 获取文件创建时间
def file_mtime(file_name):
    m_time = time.localtime(os.path.getmtime(file_name))
    local_time = str(m_time[1]) + '/' + str(m_time[2]) + '/' + str(m_time[0])
    return local_time

# 获取文件对应版本号
def get_version_number(filename):
    fileversion = '0.0.0.0'
    try:
        info = win32api.GetFileVersionInfo(filename, "\\")
        # print("info:{}".format(info))
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        # print(HIWORD(ms))
        fileversion = str(win32api.HIWORD(ms)) + '.' + str(win32api.LOWORD(ms)) + '.' + str(win32api.HIWORD(ls)) + '.' + str(win32api.LOWORD(ls))
        # return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
        return fileversion
    except:
        # return 0,0,0,0
        return fileversion