import os
import subprocess
import time
import pywinauto
import pyautogui
from pywinauto.application import Application
from pywinauto import Desktop


def test_detail_info(name):
    top_windows = Desktop(backend="uia").windows()  # or backend="win32" by default
    dlg = None
    Language = None
    try:
        for w in top_windows:
            if len(w.window_text()):
                pass

            if w.window_text() == name:
                Language = 'Chinese'
                dlg = w
                check_signture_name = '数字签名'
                check_name = '详细信息'

            elif w.window_text() == 'Security Catalogue':
                Language = 'English'
                dlg = w
            elif w.window_text() == 'Security Catalog':
                Language = 'ARM'
                dlg = w
        app = Application(backend="uia").connect(process=dlg.process_id())

        dlg = app.window(title=name)

        dlg.child_window(title=check_name, control_type="TabItem").select()
        item_detail_list = dlg.descendants(control_type="Text")
        check_detail_list = []
        for i in item_detail_list:
            a = i.window_text().split(r'uia_controls.StaticWrapper - ')[-1].split(', Static')
            check_detail_list.append(a)
        for i in range(len(check_detail_list)):
            if '版权' in check_detail_list[i]:
                print(str(check_detail_list[i + 1]))
                if "['Copyright (C)2024 NetPrisma Inc.']" == str(check_detail_list[i + 1]):
                    print('版权信息为Copyright (C)2024 NetPrisma Inc.，符合预期')
                else:
                    print(f'版权信息检查为{check_detail_list[i + 1]}，不符合预期')
            elif 'Quectel' in check_detail_list[i]:
                print(f'检查到详细信息中{check_detail_list[i - 1]}：{check_detail_list[i]}存在敏感词')
        dlg.child_window(title=check_signture_name, control_type="TabItem").select()
        item_signture_list = dlg.descendants(control_type="Text")
        check_signture_list = []
        for i in item_signture_list:
            a = i.window_text().split(r'uia_controls.StaticWrapper - ')[-1].split(', Static')
            check_signture_list.append(a)
        for i in range(len(check_detail_list)):
            if 'Quectel' in check_detail_list[i]:
                print(f'检查到详细信息中{check_detail_list[i - 1]}：{check_detail_list[i]}存在敏感词')
    finally:
        dlg.child_window(title='关闭').click()

def close_file(name):
    top_windows = Desktop(backend="uia").windows()  # or backend="win32" by default

    dlg = None

    for w in top_windows:
        if len(w.window_text()):
            pass

        if w.window_text() == name:
            dlg = w
    app = Application(backend="uia").connect(process=dlg.process_id())
    dlg = app.window(title=name)
    dlg.child_window(title='关闭').click()


def open_file_properties(path):
    # 使用subprocess调用explorer.exe，使其打开并高亮显示文件
    subprocess.run(["explorer.exe", "/select,", path])

    # 等待一段时间，确保文件或文件夹已经被选中
    time.sleep(2)

    # 发送Alt + Enter组合键
    pyautogui.hotkey('alt', 'enter')
    close_file('fw')

def traverse_files(driver_path, target_file):
    results = []
    for dirpath, dirnames, filenames in os.walk(driver_path):
        for filename in filenames:
            if target_file in str(filename):
                results.append(os.path.join(dirpath, filename))
    if results == []:
        return False
    else:
        return results


path = r'C:\Users\Lecter.zhang\Desktop\临时文件\NetPrisma_Windows_PCIE_Driver_FCUN69-WWD_Lenovo_V1.3.0.3_V06'
# open_file_properties(path)
file_types = ['.exe', '.sys', '.dll']
file_list = []
for file_type in file_types:
    k = traverse_files(path, file_type)
    file_list.append(k)
print(file_list)
for file_path in file_list:
    name = file_path.split('\\')[-1] + ' ' + '属性'
    open_file_properties(path)
    test_detail_info(name)