'''
A TestStep that involves REST API
'''
import json
import jsondiff
import requests
from collections import namedtuple
from datetime import datetime
from enum import Enum, auto
from traceback import format_exc
from typing import List, Any
from gtf.common import utils
from gtf.common.logger import Logger as logger
import gtf.core.test_base as TestBase

TAG = 'ApiStep'

Endpoint = namedtuple('Endpoint', 'Method URL')


class RequestMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class ApiStepValidation(TestBase.Validation):
    '''
    Validation for API Step
    '''
    def __init__(self, test_step):
        '''
        Defines what validation to do after a step
        
        Args:
            test_step (ApiStep): The test step for which this validation is to be done
        '''
        self.test_step = test_step
        self.status = TestBase.ValidationStatus.PASSED
        self.message = ''
    
    
    def __str__(self):
        return '{} {}. {}'.format(self.test_step.name, self.status.name.title(), self.message)
    
    
    def is_passed(self):
        """Returns whether the validations have passed or failed
        """
        return self.status.value
        
    
    # TODO: QAA-1072: Implement validations for other validation types
    
    
    def validate_response_code(self, expected_codes=[200]):
        """Validate response status code for the API step
        
        Args:
            expected_codes (list, optional): A list of accepted response codes for the request. Defaults to [200].
        """
        logger.log_info(TAG, '{}: Starting validation for response code'.format(self.test_step.name))
        if self.test_step.response.response_code in expected_codes:
            return True
        else:
            self.message += 'Response code validation failed. Expected: {}, Actual: {}'.format(expected_codes, self.test_step.response.response_code)
            self.status = TestBase.ValidationStatus.FAILED
            return False


    def validate_jsons_for_equality(self, expected, actual):
        """Validate 2 JSON objects to see if they are equal
        
        Args:
            expected (dict): Expected JSON value
            actual (dict): Actual JSON value to compare
        """
        logger.log_info(TAG, '{}: Starting validation for JSON Comparison'.format(self.test_step.name))
        dff = jsondiff.diff(expected, actual)
        if dff is None:
            return True
        else:
            self.message += 'JSON Comparison failed.'      # No expected and actual because they could be too large
            self.status = TestBase.ValidationStatus.FAILED
            return False
    
    
    def validate_json_value(self, jmes_path, expected, case_sensitive=False):
        """Validate a value in the response JSON referred to by the JMES Path
        
        Args:
            jmes_path (str): JMES Path to the actual value in the response JSON
            expected (Any): Expected value
        """
        logger.log_info(TAG, '{}: Starting validation for JSON Comparison'.format(self.test_step.name))
        actual = utils.resolve_jmes(jmes_path, json.loads(self.test_step.response.response_body))
        
        if not case_sensitive and isinstance(actual, str) and isinstance(expected, str):
            actual = actual.lower()
            expected = expected.lower()
        
        if actual == expected:
            return True
        else:
            self.message += 'JSON value Comparison failed for field {}. Expected: {}, Actual: {}'.format(jmes_path, expected, actual)
            self.status = TestBase.ValidationStatus.FAILED
            return False


class ApiStep(TestBase.TestStep):
    '''
    A test step that does some API call
    '''
    def __init__(self, url: str, endpoint: Endpoint, headers, body: Any=None, name='step'):
        '''
        Constructor for ApiStep
        
        Args:
            url (str): Base URL of the server
            endpoint (Endpoint): Target URL and HTTP Method
            headers (Dict[str, str]): HTTP request headers
            body (Any, optional): Defaults to None. Request body (Applicable for POST/PUT)
            name (str, optional): An optional name to describe what the step is doing
        '''
        # Work-around to avoid Enum comparison issues across modules
        # See https://stackoverflow.com/questions/26589805/python-enums-across-modules for info
        self.action = RequestMethod[endpoint.Method.name]
        self.target = url + endpoint.URL
        self.headers = headers
        self.body = body
        self.name = name
        self.response = None
        self.duration = 0


    def execute(self):
        '''
        Sends the HTTP request and stores the response
        '''
        logger.log_info(TAG, '{} - starting execution'.format(self.name))
        start_time = datetime.now()

        if self.action is RequestMethod.GET:
            r = requests.get(self.target, headers=self.headers)
        elif self.action is RequestMethod.POST:
            r = requests.post(self.target, json=self.body, headers=self.headers)
        elif self.action is RequestMethod.PUT:
            r = requests.put(self.target, json=self.body, headers=self.headers)
        elif self.action is RequestMethod.DELETE:
            r = requests.delete(self.target, headers=self.headers)
        else:
            raise NotImplementedError('ActionType unknown for ApiStep')
        
        # r.raise_for_status()
        response_tuple = namedtuple('response_tuple', ['response_code', 'response_body'])
        self.response = response_tuple(r.status_code, r.text)
        
        end_time = datetime.now()
        self.duration = end_time - start_time
        logger.log_info(TAG, '{} - finished execution in {} seconds'.format(self.name, self.duration.seconds))


    def save_response_to_file(self, file_path):
        """
        Saves the response of the API request to a file
        
        Args:
            file_path (str): File path to where the response should be saved
        """
        try:
            with open(file_path, 'w') as outf:
                json.dump(json.loads(self.response.response_body), outf, indent=4)
        except IOError:
            logger.log_error(TAG, 'Could not save response to file. Check if path exists and you have permission')
            logger.log_exception(TAG)
        except json.decoder.JSONDecodeError:
            logger.log_warn(TAG, 'Response not in JSON format:\n' + self.response.response_body)



# End of classes. The below method(s) are directly in the module

def get_endpoint(endpoints_reader, request_name, *args, **kwargs):
    '''
    Returns the URL endpoint for a request by reading from the Endpoints excel file
    
    Args:
        endpoints_reader (gtf.common.excel_reader.ExcelReader): obj of ExcelReader that has the Endpoints file
        request_name (str): Name of the request in module.request format. Ex: list intents will be Intents.List
        *args: args to format in the url if the url has params
        **kwargs: kwargs to format in the url if the url has params
    '''
    module, request = request_name.split('.')
    endpoints_reader.read_sheet(module, 'Name')
    method = endpoints_reader.get_value(request, 'Method')
    method = RequestMethod[method]
    url = endpoints_reader.get_value(request, 'URL').format(*args, **kwargs)
    return Endpoint(method, url)
