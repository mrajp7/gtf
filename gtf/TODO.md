## Create the following dir structure:

* core
  * test.py
    * A test is represented by an input file (from a user's perpective). The file says what tests to run
    * This has the following classes
      * TestSuite
        * A test-suite is a collection of test cases, a setup and a teardown
      * TestCase
        * A test case is a collection of steps that form a test case. While this could be just a list, having a class helps in storing metadata like result of the test-case, time taken and any other info required.
      * TestStep
        * This is a simple test step which could be one of web/mobile/api step
  * web_step.py
    * A web step is a very small fragment - a simple click of a button/entering some text, and validating the expected behavior, if any
    * This should have code that interacts with browser.
    * Should have very basic functions like 
      * opening/closing browser
      * Going to a web page
      * Checking for an element
      * Clicking on element
      * Fill a form
      * Any simple stuff that can be seen as a single step in a detailed test case, parameterized so that it can be reused.
  * api_step.py
    * An API step is an API call, and validating the response
    * Code that works as a wrapper for requests library
      * Make a request (GET/POST/PUT/DELETE and whatever)
      * Allows to set headers
      * Records time taken for the request
      * Check for a response code
      * Check for response type, maybe? (Like response must be JSON)
      * Download a file (from an API) if the response is a downloadable file, instead of HTTP body
      * Upload a file as a POST request
  * mobile_step.py
    * A mobile step could be a simple step if it is an UI step, or it could be importing/exporting a file, reading logs, etc
    * Wrapper for the mobile testing libraries (Appium/ADB)
* common
  * exceptions.py
    * This file should contain the custom excpetion classes that needs to be handled in the other code.
  * csv_file.py
    * Should support different modes of reading/writing CSV (Dict/row-column based)
  * excel_file.py
  * json_file.py


## Guidelines for the code

* All the built-in exceptions should be caught in the core. Then throw custom exceptions which needs to be handled by the projects' code
* The structure must be like this:
  * A test-suite can have multiple test cases, each having several steps
  * A test-suite is executed by the GTF
  * Before the test-suite is executed a test_setup is executed (For instance reading the intents list/dialogue_rules from PMP for Omega/Eliza)
  * After completing the test-suite, a teardown is executed (generating report, finalizing/calculating test metrics, closing open files, etc)
  * The setup and teardown must be project-specific