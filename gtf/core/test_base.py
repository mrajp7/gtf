'''
This file has the abstract classes that define the structure required to run a test.
'''

from abc import ABC, abstractmethod
from enum import Enum, auto
from datetime import datetime
from typing import List, Any


class ActionType(Enum):
    '''
    To define what action needs to be done in a test step
    '''
    pass


class ValidationStatus(Enum):
    '''
    Validation status: Could be Passed or Failed
    '''
    # We can just use boolean. But this is more readable
    FAILED = False
    PASSED = True
    
    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return super().__eq__( other)
        else:
            return self.value == other.value


class Validation:
    '''
    This is to specify what validation needs to be done, after executing a test step
    '''
    pass


class TestStep(ABC):
    '''
    This class represents a single test step.
     - what step to execute and what to validate
    '''
    # TODO: Add constructor. Let's have the following members:
    # do - what action to perform (this can be another class, which is again implemented differently for different platforms)
    # validate - what to check after the step (this can be a list so that multiple validations can be supported)
    # status - pending/skipped/running/completed (should we include passed/failed here or separately?)
    # execution_summary - contains all info about the execution - how long it took, status of individual validations, overall step_result
    
    def __init__(self, action: ActionType, target: Any, name: str='step'):
        '''
        Constructor for TestStep
        
        Args:
            action (ActionType): What action to do in this step
            target (Any): Target (object) of the action to perform
                            This could be a URL in API, a button/from on UI
            name (str): An optional name to describe what the step is doing
        '''
        self.action = action
        self.target = target
    
    
    @abstractmethod
    def execute(self):
        '''
        Method where the execution of test step happens.
        '''
        pass

