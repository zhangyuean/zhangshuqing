import os
import subprocess
import time
import pywinauto
import pyautogui
from pywinauto.application import Application
from pywinauto import Desktop
import win32api
import win32con


def test_detail_info(path):
    try:
        n = 0
        top_windows = Desktop(backend="uia").windows()  # or backend="win32" by default
        dlg = None
        for w in top_windows:
            if len(w.window_text()):
                pass

            if '属性' in w.window_text():
                name = path.split('\\')[-1] + ' ' + '属性'
                print(f'name:{name}')
                time.sleep(1)
                if w.window_text() == name:
                    dlg = w
                    check_signture_name = '数字签名'
                    check_name = '详细信息'

            elif 'Properties' in w.window_text():
                name = path.split('\\')[-1] + ' ' + 'Properties'
                print(f'name:{name}')
                time.sleep(1)
                if w.window_text() == name:
                    dlg = w
                    check_signture_name = 'Digital Signatures'
                    check_name = 'Details'
        app = Application(backend="uia").connect(process=dlg.process_id())

        dlg = app.window(title=name)

        dlg.child_window(title=check_name, control_type="TabItem").select()
        item_detail_list = dlg.descendants(control_type="Text")
        check_detail_list = []
        for i in item_detail_list:
            a = i.window_text().split(r'uia_controls.StaticWrapper - ')[-1].split(', Static')
            check_detail_list.append(a)
        for i in range(len(check_detail_list)):
            if '版权' in check_detail_list[i] or 'Copyright' in check_detail_list[i]:
                print(str(check_detail_list[i + 1]))
                if "['Copyright (C)2024 NetPrisma Inc.']" == str(check_detail_list[i + 1]):
                    print('版权信息为Copyright (C)2024 NetPrisma Inc.，符合预期')
                else:
                    print(f'版权信息检查为{check_detail_list[i + 1]}，不符合预期')
                    n += 1
            elif 'Quectel' in str(check_detail_list[i]):
                print(f'检查到详细信息中{check_detail_list[i - 1]}：{check_detail_list[i]}存在敏感词')
                n += 1
        dlg.child_window(title=check_signture_name, control_type="TabItem").select()
        item_signture_list = dlg.descendants(control_type="Text")
        check_signture_list = []
        for i in item_signture_list:
            a = i.window_text().split(r'uia_controls.StaticWrapper - ')[-1].split(', Static')
            check_signture_list.append(a)
        for i in range(len(check_signture_list)):
            if 'Quectel' in str(check_signture_list[i]):
                print(f'检查到数字签名中{check_signture_list[i]}存在敏感词')
                n += 1

        close_file()
        time.sleep(1)
        close_file()
        if not n:
            return False
        else:
            return True

    except Exception as e:
        # 捕捉所有其他类型的异常
        print(f"An error occurred: {e}")


# def close_file(name,title):
#     top_windows = Desktop(backend="uia").windows()  # or backend="win32" by default
#
#     dlg = None
#
#     for w in top_windows:
#         if len(w.window_text()):
#             pass
#
#         if w.window_text() == name:
#             dlg = w
#     app = Application(backend="uia").connect(process=dlg.process_id())
#     dlg = app.window(title=name)
#     dlg.child_window(title=title).click()


def close_file():
    # 发送 Alt 键
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    # 发送 F4 键
    win32api.keybd_event(win32con.VK_F4, 0, 0, 0)
    # 释放 F4 键
    win32api.keybd_event(win32con.VK_F4, 0, win32con.KEYEVENTF_KEYUP, 0)
    # 释放 Alt 键
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

def open_file_properties(path):
    # 使用subprocess调用explorer.exe，使其打开并高亮显示文件
    subprocess.run(["explorer.exe", "/select,", path])

    # 等待一段时间，确保文件或文件夹已经被选中
    time.sleep(2)

    # 发送Alt + Enter组合键
    pyautogui.hotkey('alt', 'enter')

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


path = r'C:\Users\Lecter.zhang\Desktop\临时文件\Quectel_Windows_PCIE_Driver_RM520NGL_Samsung_V1.3.0.4_V02'
file_types = ['.exe', '.sys', '.dll']
file_list = []
for file_type in file_types:
    k = traverse_files(path, file_type)
    file_list.append(k)
result = 0
for file_path in file_list:
    for file in file_path:
        if 'libcrypto-1_1-x64.dll' in file or 'vcruntime140.dll' in file:
            file_name = file.split("\\")[-1]
            print(f'文件{file_name}非公司文件，不做检查')
            pass
        else:
            open_file_properties(file)
            time.sleep(3)
            if not test_detail_info(file):
                result += 1
# name = path.split('\\')[-1] + ' ' + '属性'
# open_file_properties(path)
# time.sleep(3)
# test_detail_info(name)
