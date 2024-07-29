import subprocess
import os

path = r'C:\Users\Lecter.zhang\Desktop\临时文件\NetPrisma_Windows_PCIE_Driver_FCUN69-WWD_Lenovo_V1.3.0.3_V06\windows\fw\mbfwdriverfcun69wwd.cat'

def check_cat_sigature(path):
    cmd = f'certutil -dump {path}'
    out = subprocess.check_output(cmd, text= True, errors='ignore')
    line = out.splitlines()
    n = 0
    for i in line:
        if 'Quectel' in i:
            print(f'检查到cat文件{path}中存在敏感词:{i}')
            n += 1
    if not n:
        return True
    else:
        return False

if check_cat_sigature(path):
    print(1111)

