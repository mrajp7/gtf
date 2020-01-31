import json
import logging
import copy
import os
import re
import traceback
import unittest
from collections import defaultdict
from nose2.events import Plugin
from datetime import datetime

from .render import load_template, render_template

logger = logging.getLogger(__name__)


class HTMLReporter(Plugin):
    configSection = 'html-report'
    commandLineSwitch = (None, 'html-report', 'Generate an HTML report containing test results')

    def __init__(self, *args, **kwargs):
        super(HTMLReporter, self).__init__(*args, **kwargs)
        self.summary_stats = defaultdict(int)
        self.module_wise_summary = {}
        self.module_wise_test_results = {}
        self.test_results = []
        self.total_summary = {}
        default_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'report.html') 

        self._config = {
            'report_path': os.path.realpath(self.config.as_str('path', default='report.html')),
            'template':  os.path.realpath(self.config.as_str('template', default=default_template_path)),
            'module_re': self.config.as_str('module_re', default='.*_(.*)')
        }
        logger.info('HTML report path: ' + self._config['report_path'])

    def _sort_test_results(self):
        return sorted(self.test_results, key=lambda x: x['name'])
    

    def _generate_search_terms(self):
        """
        Map search terms to what test case(s) they're related to

        Returns:
            dict: maps search terms to what test case(s) it's relevant to

        Example:
        {
            '12034': ['ui.tests.TestSomething.test_hello_world'],
            'buggy': ['ui.tests.TestSomething.test_hello_world', 'ui.tests.TestSomething.buggy_test_case'],
            'ui.tests.TestAnother.test_fail': ['ui.tests.TestAnother.test_fail']
        }
        """
        search_terms = {}

        for test_result in self.test_results:
            # search for the test name itself maps to the test case
            search_terms[test_result['name']] = test_result['name']

            if test_result['description']:
                for token in test_result['description'].split():
                    if token in search_terms:
                        search_terms[token].append(test_result['name'])
                    else:
                        search_terms[token] = [test_result['name']]

        return search_terms

    def testOutcome(self, event):
        """
        Reports the outcome of each test
        """
        test_case_import_path = event.test.id()
        module = test_case_import_path.split('_')[-1]       # Default module selection
        
        # Try to read module name from configure RE
        if hasattr(event.test, 'module'):
            module = event.test.module
        else:
            mo = re.search(self._config['module_re'], test_case_import_path)
            if mo:
                module = mo.group(1)
        
        if module not in self.module_wise_summary:
            self.module_wise_summary[module] = defaultdict(int)
            self.module_wise_test_results[module] = []

        # Ignore _ErrorHolder (for arbitrary errors like module import errors),
        # as there will be no doc string in these scenarios
        test_case_doc = None
        failure_reason = 'None'
        if not isinstance(event.test, unittest.suite._ErrorHolder):
            test_case_doc = event.test.shortDescription()

        formatted_traceback = None
        if event.outcome in ['failed', 'error']:
            if event.exc_info:
                exception_type = event.exc_info[0]
                exception_message = event.exc_info[1]
                exception_traceback = event.exc_info[2]
                formatted_traceback = ''.join(traceback.format_exception(
                    exception_type, exception_message, exception_traceback))
                failure_reason = str(exception_message).split(':')[-1].strip()
        elif event.outcome == 'skipped':
            failure_reason = event.reason

        self.module_wise_summary[module][event.outcome] += 1
        self.summary_stats[event.outcome] += 1

        test_result = {
            'name': test_case_import_path,
            'test_name': event.test.test_name if (hasattr(event.test, 'test_name') and event.test.test_name) \
                                              else test_case_import_path,
            'description': test_case_doc,
            'result': event.outcome,
            'traceback': formatted_traceback,
            'metadata': copy.copy(event.metadata),
            'failure_reason': failure_reason
        }
        self.test_results.append(test_result)
        self.module_wise_test_results[module].append(test_result)


    def afterSummaryReport(self, event):
        """
        After everything is done, generate the report
        """
        logger.info('Generating HTML report...')

        sorted_test_results = self._sort_test_results()
        test_title = 'Test Report'
        if len(sorted_test_results) > 0:
            test_title += ' - ' + sorted_test_results[0]['name'].split('.')[0]
            self.total_summary['total'] = sum(self.summary_stats.values())
            self.total_summary['Pass Percentage'] = round(self.summary_stats['passed'] / self.total_summary['total'] * 100, 2)

        context = {
            'test_report_title': test_title,
            'test_summary': self.summary_stats,
            'total_summary': self.total_summary,
            'module_wise_summary': self.module_wise_summary,
            'module_wise_test_results': self.module_wise_test_results,
            'test_results': sorted_test_results,
            'autocomplete_terms': json.dumps(self._generate_search_terms()),
            'timestamp': datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S UTC')
        }
        template = load_template(self._config['template'])
        rendered_template = render_template(template, context)
        with open(self._config['report_path'], 'w') as template_file:
            template_file.write(rendered_template)
