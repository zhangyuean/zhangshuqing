import pyautogui
import time


def get_click_position_and_click():
    print("5s内将鼠标放到需要点击的位置")
    time.sleep(5)
    x, y = pyautogui.position()
    return x, y


a = []
b = int(input('please input the number of position to click：'))
c = int(input('please input waiting time of every cycle:'))
for i in range(b):
    b = get_click_position_and_click()
    a.append(b)

print('获取到所有位置，开始点击')
n = 1
while True:
    for i in range(c):
        time.sleep(1)
        print(f'{c-i}s后开始点击')
    if n < 300:
        for i in a:
          time.sleep(2)
          pyautogui.click(i)
        n += 1
        print(f'runtimes:{n}')
    else:
        break