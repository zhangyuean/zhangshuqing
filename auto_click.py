import pyautogui
import time


def get_click_position_and_click():
    print("put mouse to the position you want to click in 5s")
    time.sleep(5)
    x, y = pyautogui.position()
    return x, y


a = []
b = int(input('please input the number of position to click：'))
c = int(input('please input waiting time of every cycle:'))
d = int(input('please input runtimes:'))
for i in range(b):
    b = get_click_position_and_click()
    a.append(b)

print('get all position，start click')
n = 1
while True:
    for i in range(c):
        time.sleep(1)
        print(f'start click after {c-i}s')
    if n < 300:
        for i in a:
          time.sleep(2)
          pyautogui.click(i)
        n += 1
        print(f'runtimes:{n}')
    else:
        break