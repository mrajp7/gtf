import json
import logging
import copy
import getpass
import os
import re
import traceback
import unittest
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict
from nose2.events import Plugin
from datetime import datetime

from .render import load_template, render_template

logger = logging.getLogger(__name__)

# --- TEST SUMMARY STAT ---
#Test Run title 
#Triggered by
#Total Tests
#Passed
#Failed
#Others
#Passed %
#Failed %

# --- MODULE SUMMARY STAT ---
#Module Name
#Total Tests
#Passed
#Failed
#Others


class EmailReporter(Plugin):
    configSection = 'email-report'
    commandLineSwitch = (None, 'email-report', 'Generate an email report containing test results')

    def __init__(self, *args, **kwargs):
        super(EmailReporter, self).__init__(*args, **kwargs)
        self.module_wise_summary = {}
        self.total_summary = defaultdict(int)
        default_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'email_report.html') 

        self._config = {
            'template':  os.path.realpath(self.config.as_str('template', default=default_template_path)),
            'module_re': self.config.as_str('module_re', default='.*_(.*)'),
            'smtp' : self.config.as_str('smtp',default=''),
            'username' : self.config.as_str('email',default=''),
            'password' : self.config.as_str('password',default=''),
            'recipient' : self.config.as_list('recipients',default=''),
            'port' : self.config.as_str('port',default=''),
            'from' : self.config.as_str('from',default='')
        }

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

        self.module_wise_summary[module][event.outcome] += 1
        self.total_summary[event.outcome] += 1
       
    def afterSummaryReport(self, event):
        """
        After everything is done, generate the report
        """
        logger.info('Generating Email report...')

        test_title = 'Test Report'
        if len(self.total_summary) > 0:
            self.total_summary['total'] = sum(self.total_summary.values())
            self.total_summary['Pass Percentage'] = round(self.total_summary['passed'] / self.total_summary['total'] * 100, 2)
            self.total_summary['Fail Percentage'] = round(self.total_summary['failed'] / self.total_summary['total'] * 100, 2)
        
        for module in self.module_wise_summary:
            self.module_wise_summary[module]['total'] = sum(self.module_wise_summary[module].values())
            self.module_wise_summary[module]['other'] = self.module_wise_summary[module]['total'] - (self.module_wise_summary[module]['passed'] + self.module_wise_summary[module]['failed'])

        self.context = {
            'test_report_title': test_title,
            'triggered_by': getpass.getuser().title(),
            'total_summary': self.total_summary,
            'module_wise_summary': self.module_wise_summary,
            'timestamp': datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S UTC')
        }
        template = load_template(self._config['template'])
        rendered_template = render_template(template, self.context)
        """ with open("output/email_report.html", 'w') as template_file:
            template_file.write(rendered_template) """
        self.send_email(rendered_template)
        
    def send_email(self,body):
        sender_email = self._config['from']
        receiver_email = self._config['recipient']
        password = self._config['password']

        message = MIMEMultipart("alternative")
        message["Subject"] = "Test Run report " + self.context['timestamp']
        message["From"] = sender_email
        message["To"] = ','.join(receiver_email)

        part2 = MIMEText(body, "html")

        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
