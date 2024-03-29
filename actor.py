from controller import Controller
from configparser import ConfigParser
import time
class Actor:
    
    def __init__(self, _stopevent, setStatus, parent):
        self._stopevent = _stopevent
        self.setStatus = setStatus
        self.parent = parent
        self.config_filename = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_filename)
        self.controller = Controller(self.config, self.setStatus, self.parent)

    def clickButton_Name(self, button_name):
        self.controller.mouse_click_name(button_name)
    def key_input(self, s):
        self.controller.key_input(s)
    def key_remove(self, s):
        self.controller.key_remove(s)
    
    def follow_one(self):
        self.controller.mouse_click_name('item')
        time.sleep(1)
        name = self.controller.capture_text('item_name')
        name_list = name.split()
        time.sleep(1)
        self.controller.mouse_click_name('back')
        if len(name_list) == 0:
            return ''
        self.controller.mouse_click_name('item_follow')
        return name_list[0]

    def unfollow_one(self, name):
        self.controller.mouse_click_name('item_unfollow')

    def backFromCancel(self):
        [ret, rect] = self.controller.pattern_match('cancel')
        if ret:
            self.controller.mouse_click_name('search_cancel')
            return True
        return False
    
    def backFromBack(self):
        [ret, rect] = self.controller.pattern_match('back') 
        if ret:
            self.controller.mouse_click_name('back')
            return True
        return False

    def capture_search_result(self, type):
        [follow_status, full_status] = self.controller.capture_color(type)

        key_word = 'search_result'
        if type == 'specified_follow':
            key_word = 'specified_result'
        name = self.controller.capture_text(key_word)
        search_status = True
        print('name->',name)
        if (full_status > 253) or ('found' in name) or ('for you' in name) or (name is ''):
            search_status = False

        return [search_status, follow_status]

    def remove_block(self):
        while True:
            name = self.controller.capture_text('blocked')
            if 'Action Blocked' not in name:
                break
            self.controller.mouse_click_name('block_ok')
            time.sleep(0.5)

    def get_config(self, val1, val2):
        return int(self.config.get(val1, val2))
    def save_config(self):
        with open(self.config_filename, 'w') as f:
            self.config.write(f + '\n')
        
    def find_click(self, key_name, delay):
        self.controller.main_drag()
        time.sleep(delay)
        [ret, rect] = self.controller.pattern_match(key_name)
        # print('FIND RESULT ', key_name, ret, rect)
        time.sleep(2)
        if ret:
            self.controller.pattern_click(key_name, 'heart', rect)
            return

    def check_captured_text(self, item_name, text):
        res_text = self.controller.capture_text(item_name).lower()
        print('[SPIDER] [captured_result] ', '<'+res_text+'>', '<'+text+'>')
        return res_text == text


    
