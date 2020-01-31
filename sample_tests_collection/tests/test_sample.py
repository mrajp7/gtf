
import unittest
from sample_tests_collection.layers import BaseLayer


class SampleTest(unittest.TestCase):
    """This is a test class.
    A test class needs to inherit unittest.TestCase
    """
    # We need to specify the layer property to the Layer class where the test fixtures are defined
    layer = BaseLayer
    
    # The module property helps the test reporter group the test results by module 
    # and to report a test summary for each module
    module = 'Sample'
    
    def test_something(self):
        """This is a sample test method
        A test is a method that starts with test_
        """
        # Inheriting from unittest.TestCase provides a number of assert methods.
        # The assert methods can check for some values or conditions.
        # When they are not as expected, the assert methods will make the test fail
        
        # This is a sample assert method that checks its first argument evaluates to True
        # Since it is True here, this test will pass
        self.assertTrue(True, 'Some message to print when assert fails')
    
    
    def test_that_fails(self):
        """This is a sample test that will fail
        """
        # A test will fail if an assert condition does not match.
        self.assertEqual(2+1, 3, 'This should pass')
        self.assertNotEqual(2-1, 3, 'This will also pass')
        with self.assertRaises(ZeroDivisionError):
            # This is a way to check if an expected exception is raised when an invalid operation is done
            print(5 / 0)
        
        # This step will fail
        self.assertTrue([], 'An empty list evaluates to False')
    
    
    def test_with_error(self):
        """A test reports error if there's an exception
        """
        self.assertEqual(5 / 0, 0, 'Dividing by zero is going to cause trouble')