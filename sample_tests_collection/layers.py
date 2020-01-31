"""
This file is to define the test fixtures (as layers)
"""

import gtf.common.utils as utils
from gtf.common.logger import Logger as logger
from sample_tests_collection.config_manager import TestConfig

#region for remote debugging
import ptvsd

# 5678 is the default attach port in the VS Code debug configurations
print("Waiting for debugger attach")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach(10)   # Wait for 10 seconds, and continue if not attached within that
breakpoint()
#endregion

TAG = 'BaseLayer'

class BaseLayer(object):
    """
    This layer will be the base layer for all other layers.
    Here, we need to include the setup that needs to be done before any of the tests are run
    """
    
    @classmethod
    def setUp(cls):
        """
        The setUp method should always be a classmethod.
        We should create an output folder where the report and the logs will be saved.
        We should initialize the logger here.
        We should initialize the config reader, if any.
        """
        logger.log_info(TAG, 'BaseLayer setUp')
        
        # Initialize and read the configuration
        TestConfig.init_config()

        # Create a test run dir
        TestConfig.output_dir = utils.create_time_stamped_dir(path='./output', prefix='test_run')
        # Set up the logger
        logger.init_log_to_file(TestConfig.output_dir)
    
    
    @classmethod
    def tearDown(cls):
        """
        The tearDown should always be a classmethod
        In the tearDown, we cleanup the resources used in the tests
        In this case, we close the log file
        """
        logger.log_info(TAG, 'BaseLayer tearDown')
        logger.close_log_file()


class DerivedLayer(BaseLayer):
    """
    This is a layer that is derived from the BaseLayer
    When a TestCase class uses this layer for fixtures, 
        - BaseLayer setup runs
        - DerivedLayer setup runs
        - All tests that uses DerivedLayer for fixtures run
        -DerivedLayer tearDownn
        -BaseLayer tearDown

    """
    
    @classmethod
    def setUp(cls):
        logger.log_info(TAG, 'DerivedLayer setUp - Doing nothing here')
    
    
    @classmethod
    def tearDown(cls):
        logger.log_info(TAG, 'DerivedLayer tearDown - This runs before BaseLayer tearDown')
        
    
    @classmethod
    def testSetUp(cls, test):
        """
        A testSetUp is run before EACH test that uses this layer
        
        Args:
            test (test class): The test class that is running
        """
        logger.log_info(TAG, 'DerivedLayer testSetUp')
        if hasattr(test, 'needs_prep'):
            if test.needs_prep:
                logger.log_info(TAG, 'Doing some special preperation for some tests where an attribute is set')