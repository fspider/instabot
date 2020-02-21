import win32api, win32con
import cv2
import numpy as np
from PIL import ImageGrab
import win32gui
import time
from vk_code import *
import pytesseract

class Controller:

    def __init__(self, config, setStatus):
        self.config = config
        self.setStatus = setStatus
        self.windows_list = []
        self.toplist = []

        def enum_win(hwnd, result):
            win_text = win32gui.GetWindowText(hwnd)
            self.windows_list.append((hwnd, win_text))

        win32gui.EnumWindows(enum_win, self.toplist)
        # Game handle
        game_hwnd = 0
        for (hwnd, win_text) in self.windows_list:
            if "bluestacks" in win_text.lower():
                game_hwnd = hwnd

        self.position = win32gui.GetWindowRect(game_hwnd)
        print(self.position)

        self.padding_x = float(self.config.get('points', 'padding_x'))
        self.padding_y = float(self.config.get('points', 'padding_y'))
        self.mouse_delay = float(self.config.get('main', 'mouse_delay'))
        self.keyinput_delay = float(self.config.get('main', 'keyinput_delay'))
        self.keyremove_delay = float(self.config.get('main', 'keyremove_delay'))
        self.keyboard_delay = float(self.config.get('main', 'keyboard_delay'))
        self.item_down_delay = float(self.config.get('main', 'item_down_delay'))
        if self.config.get('main', 'face_book') == 'yes':
            self.face_book = True
        else:
            self.face_book = False


        pytesseract.pytesseract.tesseract_cmd = self.config.get('main', 'tesseract_path')

        self.x = self.position[0]
        self.y = self.position[1]
        self.w = self.position[2] - self.position[0] - self.padding_x
        self.h = self.position[3] - self.position[1] - self.padding_y

    def get_name_pos(self, button_name):
        if not self.face_book:
            if button_name == 'discover':
                button_name = 'discover_no'

        button_x = float(self.config.get('points', button_name + '_x'))
        button_y = float(self.config.get('points', button_name + '_y'))

        bt_x = int(self.x + self.w * button_x)
        bt_y = int(self.y + self.h * button_y + self.padding_y)
        return [bt_x, bt_y]

    def mouse_click_name(self, button_name):
        [bt_x, bt_y] = self.get_name_pos(button_name)
        self.mouse_click(bt_x, bt_y)
        # print('clicked ' + button_name + ' button', bt_x, bt_y)
        time.sleep(self.mouse_delay)

    def mouse_double_click_name(self, button_name):
        time.sleep(2)
        [bt_x, bt_y] = self.get_name_pos(button_name)

        self.mouse_click(bt_x, bt_y)
        time.sleep(1)
        self.mouse_click(bt_x, bt_y)
        time.sleep(3)
        self.mouse_click(bt_x, bt_y)
        time.sleep(0.5)
        self.mouse_click(bt_x, bt_y)

        # print('clicked ' + button_name + ' button', bt_x, bt_y)
        time.sleep(self.mouse_delay)

    def mouse_click(self, x,y):
        try:
            win32api.SetCursorPos((x,y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            time.sleep(0.10)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        except Exception as e:
            print('Error with Set Cursor ', x, y, e)
    def mouse_scroll_name(self, button_name):
        [bt_x, bt_y] = self.get_name_pos(button_name)
        for i in range(7):
            self.mouse_scroll(bt_x, bt_y, -10)
            time.sleep(0.5)

    def mouse_scroll(self, x, y, clicks):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, clicks, 0)
    
    def key_input(self, str=''):
        for c in str:
            if c.isupper():
                cc = c.lower()
                win32api.keybd_event(VK_CODE['shift'], 0, 0, 0)
                win32api.keybd_event(VK_CODE[cc], 0, 0, 0)
                time.sleep(0.01)
                win32api.keybd_event(VK_CODE[cc], 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(VK_CODE['shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
            elif c=='_':
                win32api.keybd_event(VK_CODE['shift'], 0, 0, 0)
                win32api.keybd_event(VK_CODE['-'], 0, 0, 0)
                time.sleep(0.01)
                win32api.keybd_event(VK_CODE['-'], 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(VK_CODE['shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                win32api.keybd_event(VK_CODE[c], 0, 0, 0)
                time.sleep(0.01)
                win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(self.keyboard_delay)

    def ctrl_A(self):
        time.sleep(1)
        win32api.keybd_event(VK_CODE['ctrl'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['a'], 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_CODE['a'], 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(VK_CODE['ctrl'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(1)

    def key_remove(self, str):
        for c in range(20):
            win32api.keybd_event(VK_CODE['backspace'], 0, 0, 0)
            time.sleep(0.01)
            win32api.keybd_event(VK_CODE['backspace'], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(self.keyinput_delay)
        time.sleep(self.keyboard_delay)

    def item_scroll_prepare(self):
        if self.face_book:
            self.mouse_click_name('discover_plus')

        self.mouse_click_name('mid')
        self.mouse_click_name('back')
        time.sleep(3)
        for i in range(4):
            win32api.keybd_event(VK_CODE['down_arrow'], 0, 0, 0)
            time.sleep(0.01)
            win32api.keybd_event(VK_CODE['down_arrow'], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(self.keyboard_delay)
        win32api.keybd_event(VK_CODE['up_arrow'], 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_CODE['up_arrow'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(self.keyboard_delay)

        # self.item_scroll_down()


    def item_scroll_down(self):
        win32api.keybd_event(VK_CODE['down_arrow'], 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_CODE['down_arrow'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(self.keyboard_delay)
        win32api.keybd_event(VK_CODE['down_arrow'], 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_CODE['down_arrow'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(self.keyboard_delay)

        win32api.keybd_event(VK_CODE['up_arrow'], 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_CODE['up_arrow'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(self.keyboard_delay)

    def get_screen_shot(self, key_name, dx=0, dy=0):
        item_x1 = min(float(self.config.get('rect', key_name + '_x1')) + dx, 0.99)
        item_y1 = min(float(self.config.get('rect', key_name + '_y1')) + dy, 0.99)
        item_x2 = min(float(self.config.get('rect', key_name + '_x2')) + dx, 0.99)
        item_y2 = min(float(self.config.get('rect', key_name + '_y2')) + dy, 0.99)
        rect_x1 = int(self.x + self.w * item_x1)
        rect_y1 = int(self.y + self.h * item_y1 + self.padding_y)
        rect_x2 = int(self.x + self.w * item_x2)
        rect_y2 = int(self.y + self.h * item_y2 + self.padding_y)

        capture_range = (rect_x1, rect_y1, rect_x2, rect_y2)
        screenshot = ImageGrab.grab(capture_range)
        screenshot = np.array(screenshot)
        return screenshot

    def capture_color(self, key_name):
        screenshot = self.get_screen_shot(key_name)
        img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        # cv2.imshow(key_name, img)
        # cv2.waitKey(1)

        avg_color_per_row = np.average(img, axis=0)
        ac = np.average(avg_color_per_row, axis=0)
        color_delta = 5
        print(key_name, '->', ac)
        full_status = np.average(ac, axis=0)
        if abs(ac[0] - ac[1]) < color_delta and abs(ac[1] - ac[2]) < color_delta and abs(ac[0] - ac[2]) < color_delta:
            return [True, full_status]
        return [False, full_status]

    def capture_text(self, key_name):
        screenshot = self.get_screen_shot(key_name)
        img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        name = pytesseract.image_to_string(img, lang='eng')
        return name

    def img_col_count(self,key_name, dx=0, dy=0):
        screenshot = self.get_screen_shot(key_name, 0, dy)
        img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        cv2.imshow(key_name, img)
        cv2.waitKey(1)
        print(img.shape)
        ww = img.shape[0]
        hh = img.shape[1]
        if ww == 0 or hh == 0:
            return 0
        cnt = 0
        for i in range(ww):
            for j in range(hh):
                pixel = img[i][j]
                if pixel[0] == 240 and pixel[1] == 151 and pixel[2] == 56:
                    cnt += 1
        val = 1.0 * cnt / ww / hh
        print('--', val)
        return val
    def scan(self, key_name):
        max_val = 0
        max_dy = 0
        for dy in np.arange(0, 0.2, 0.005):
            val = self.img_col_count(key_name, 0, dy)
            if val> max_val:
                max_val = val
                max_dy = dy
        # print('Scan -> result', max_val, max_dy)
        self.display(key_name, 0, max_dy)
        time.sleep(1)
        cv2.destroyWindow(key_name)
        time.sleep(1)
        if max_val <0.75:
            print('---> max_val = ', max_val)
            return False
        item_x1 = min(float(self.config.get('rect', key_name + '_x1')), 0.99)
        item_y1 = min(float(self.config.get('rect', key_name + '_y1')) + max_dy, 0.99)
        item_x2 = min(float(self.config.get('rect', key_name + '_x2')), 0.99)
        item_y2 = min(float(self.config.get('rect', key_name + '_y2')) + max_dy, 0.99)
        item_x = (item_x1 + item_x2) / 2
        item_y = (item_y1 + item_y2) / 2
        bt_x = int(self.x + self.w * item_x)
        bt_y = int(self.y + self.h * item_y + self.padding_y)
        self.mouse_click(bt_x, bt_y)
        time.sleep(self.mouse_delay)
        return True


    def display(self, key_name, dx=0, dy=0):
        screenshot = self.get_screen_shot(key_name, dx, dy)
        img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        cv2.imshow(key_name, img)
        cv2.waitKey(1)

    def waitSleep(self, value):
        self.setStatus('Waiting for ' + str(value) + ' seconds while loading ...')
        time.sleep(value)
        self.setStatus('Working ...')




