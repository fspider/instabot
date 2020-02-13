from configparser import ConfigParser
class Config:
    def __init__():
        self.config_filename = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_filename)
        # config.add_section('main')
        # config.set('main', 'key1', 'value1')
    def get_config():
        return self.config
    
    def save():
        with open(self.config_filename, 'w') as f:
            config.write(f)