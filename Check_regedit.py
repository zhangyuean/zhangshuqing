import winreg

def check_registry_path_exists(hive, sub_key):
    try:
        # 尝试打开注册表键
        key = winreg.OpenKey(hive, sub_key, 0, winreg.KEY_READ)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        print(f"The specified registry path {sub_key} does not exist.")
        return False
    except PermissionError:
        print(f"Permission denied for accessing the registry path {sub_key}.")
        return False
    except WindowsError as e:
        print(f"An error occurred while trying to access the registry key: {e}")
        return False

# 定义要查询的注册表路径
hive = winreg.HKEY_LOCAL_MACHINE
sub_key = r'SOFTWARE\Microsoft\Wlpasvc'

# 检查注册表路径是否存在
exists = check_registry_path_exists(hive, sub_key)
if exists:
    print(f"The registry path {sub_key} exists.")
else:
    print(f"The registry path {sub_key} does not exist.")