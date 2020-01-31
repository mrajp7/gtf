from configobj import ConfigObj
from gtf.common.excel_reader import ExcelReader
from gtf.common.logger import Logger as logger

TAG = 'ConfigManager'

class TestConfig():
    output_dir = ''
    config_file = 'sample_tests/data/config.ini'
    
    # This is a file where we save the endpoint URL for the different API requests.
    # Similarly we need to have files for web/mobile tests where object descriptions/paths are saved
    ENDPOINTS_FILE = 'sample_tests/data/Endpoints.xlsx'
    
    @classmethod
    def init_config(cls):
        cls.config = ConfigObj(cls.config_file)
        try:
            # Reading any value from the config file
            cls.VALUE = cls.config['default']['some_key']
            
            # Initializing the Endpoints reader. Keeping it here because it will be needed across the project
            cls.endpoints_reader = ExcelReader(cls.ENDPOINTS_FILE)
        except KeyError:
            logger.log_exception(TAG)
