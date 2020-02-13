import cv2
import numpy as np
from PIL import ImageGrab
import win32gui
import time
import pytesseract
from pytesseract import Output

windows_list = []
toplist = []
def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))
win32gui.EnumWindows(enum_win, toplist)

# Game handle
game_hwnd = 0
for (hwnd, win_text) in windows_list:
    if "bluestacks" in win_text.lower():
        game_hwnd = hwnd

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

while True:
    time.sleep(0.01)
    position = win32gui.GetWindowRect(game_hwnd)
    print(position)
    # Take screenshot
    screenshot = ImageGrab.grab(position)
    screenshot = np.array(screenshot)

    img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    # print(pytesseract.image_to_string(screenshot, lang='eng'))
    # cv2.imshow("Screen", screenshot)

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    print(d)
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Screen", img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break