from controller import Controller
from configparser import ConfigParser
import time
class Actor:
    
    def __init__(self):
        self.config_filename = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_filename)
        self.controller = Controller(self.config)

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
        if len(name_list) == 0:
            return ''

        time.sleep(1)
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('item_follow')
        return name_list[0]
    
    def unfollow_one(self, name):
        self.controller.mouse_click_name('item_unfollow')

    def capture_search_result(self):
        name = self.controller.capture_text('search_result')
        print(name)
        if 'No users found' in name:
            return False
        elif name is '':
            return False
        else:
            return True

    def get_config(self, val1, val2):
        return int(self.config.get(val1, val2))
    def save_config(self):
        with open(self.config_filename, 'w') as f:
            config.write(f + '\n')
        
    
