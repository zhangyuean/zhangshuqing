
from lib.CheckFile import *
import re

path = r'C:\Users\Lecter.zhang\Desktop\临时文件\NetPrisma_Windows_PCIE_Driver_FCUN69-WWD_Lenovo_V1.3.0.3_V06\windows\auth' \
       r'\ModemAuthServiceFCUN69WWD.inf'
with open(path, 'r') as f:
       s = f.read()
       ret = re.search("DriverVer.*,", s)
       ret2 = ret[0].split(f'=')[-1].strip()[0:-1].split(f'/')
       print(f'读取到inf文件{path}修改日期为{ret2}')

