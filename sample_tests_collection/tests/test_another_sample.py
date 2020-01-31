
import unittest
from sample_tests_collection.layers import DerivedLayer


class AnotherSampleTest(unittest.TestCase):
    """This is a test class.
    A test class needs to inherit unittest.TestCase
    """
    # We need to specify the layer property to the Layer class where the test fixtures are defined
    layer = DerivedLayer
    needs_prep = True   # This is a property used to demonstrate how testSetUp can be used with test arg
    
    # This class is not using the module attribute. The module name will be taken from the class name
    # as defined by the 'module_re' key in the html-report config section in nose2.cfg
    # module = 'Sample'
    
    # We can assign a test_name property to the class
    test_name = ''
    
    
    @classmethod
    def setUp(cls):
        """This setup will run before each test"""
        # Reset the test name. If this is not done, and any of the test does not assign a name,
        # then the name from the previous test will be taken and used in the report
        cls.test_name = ''
    
    
    def test_addition(self):
        """This is a sample test method
        """
        # By adding this here, we can view this test name in the report instead of the long path
        AnotherSampleTest.test_name = 'Addition test'
        self.assertTrue(1 + 1 == 2, 'Some message to print when assert fails')
    
    
    def test_with_attribute(self):
        """This is a sample test that has some attributes
        """
        # But make sure to set it in all the test methods.
        # Otherwise it will use the name from the previous test
        # Another way is to reset the name in a testSetUp
        AnotherSampleTest.test_name = 'With attribute test'
        self.assertEqual(2+1, 3, 'This should pass')
    
    # The attributes can be used to filter some tests to run only them
    # For example this test can be run with the -E option as below:
    # nose2 -v -E 'always_run == True'
    test_with_attribute.always_run = True
