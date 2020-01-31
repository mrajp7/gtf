# generic-test-framework

The objective of this project is to create a generic test framework that can be used across different projects.

As the first phase the project focuses on API automation for Theori. Once we have the framework complete, we might add new projects to this framework

## Pre-requisites
 * install nose2 (pip3 install nose2)
 * pip3 install jmespath


## How to run tests
### To run all tests in a project
To run all the tests in the theori project, use the command:

`nose2 -v theori`


### To run the tests from a single file
If we want to run the tests only from the file theori/tests/test_faq.py, use the command:

`nose2 -v theori.tests.test_faq`


### To run a set of tests based on an attribute
Attributes can be added to test methods using the syntax:

`<test_method>.attrib = value`

To run the tests that have a specific attribute use the command
`nose2 -v -A attrib=value theori`

For example, we can have a suites attribute to the tests that can have values like gold, sanity, p2, etc. Now to run only the smoke tests:

`nose2 -v -c nose2.cfg -A suites=smoke theori`

Here, suites can be a list so that a test can be tagged in 45both in smoke and gold suites