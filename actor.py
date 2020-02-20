from controller import Controller
from configparser import ConfigParser
import time
class Actor:
    
    def __init__(self, _stopevent, setStatus):
        self._stopevent = _stopevent
        self.setStatus = setStatus
        self.config_filename = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_filename)
        self.controller = Controller(self.config, self.setStatus)

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

    def capture_search_result(self, type):
        [follow_status, full_status] = self.controller.capture_color(type)

        key_word = 'search_result'
        if type == 'specified_follow':
            key_word = 'specified_result'
        name = self.controller.capture_text(key_word)
        search_status = True
        print(name)
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
        
    
