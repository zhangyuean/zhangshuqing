from lib.Hub import delete
import time
from datetime import datetime
from functools import reduce
a = delete
driver_path = r'C:\Users\Lecter.zhang\Desktop\临时文件'
file_list = a.traverse_files(driver_path)
file_remove_list = []
for i in file_list:
    len_file_path = i.split('\\')
    file_time = a.get_file_date(i)
    time_now = datetime.fromtimestamp((int(time.time())))
    time_different = str((time_now - file_time)).split('day')
    try:
        if int(time_different[0]) > 30:
            file_remove_list.append(i)
            a.delete_file(i)
            print(i)
    except Exception:
        print(time_different)


