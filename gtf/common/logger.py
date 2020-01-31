import colorama
import datetime
import inspect
import os.path
import re
import traceback
from colorama import Fore, Back
from enum import Enum, auto

colorama.init()

class LogLevel(Enum):
    INFO = auto()
    DEBUG = auto()
    WARN = auto()
    ERROR = auto()
    CRITICAL = auto()
    VERBOSE = auto()


class Logger():

    TAG = "Logger"
    LOG_FILE_FP = None


    @classmethod
    def init_log_to_file(cls, output_path):
        """
        Create a log file to write console logs to.
        
        Args:
            output_path (str): Directory path where log file should be created
        """
        cls.LOG_FILE_FP = open(os.path.join(output_path, 'console.log'), 'w')


    @classmethod
    def close_log_file(cls):
        """
        Close the log file in the end
        """
        cls.LOG_FILE_FP.close()


    @classmethod
    def log(cls, level, tag, message):
        """
        This method defines how the logs will be printed for different log types, i.e Info, Debug, Warn, Error, Verbose and Critical.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        Args:
            log level
            tag
            message
        Returns:
            None
        """
        color = Fore.GREEN      # Default setting is INFO
        if level == LogLevel.INFO:
            color = Fore.GREEN
            tag = cls.currentTime() + " I/" + tag
        elif level == LogLevel.DEBUG:
            color = Fore.CYAN
            tag = cls.currentTime() + " D/" + tag
        elif level == LogLevel.WARN:
            color = Fore.YELLOW
            tag = cls.currentTime() + " W/" + tag
        elif level == LogLevel.ERROR:
            color = Fore.RED
            tag = cls.currentTime() + " E/" + tag
        elif level == LogLevel.VERBOSE:
            tag = cls.currentTime() + " V/" + tag
        elif level == LogLevel.CRITICAL:
            color = Fore.RED + Back.WHITE
            tag = cls.currentTime() + " C/" + tag
        
        msg = tag + '.' + str(inspect.stack()[2].lineno) + " : " + message
        formatted_msg = color + msg + Fore.RESET + Back.RESET
        print(formatted_msg)
        
        if cls.LOG_FILE_FP:
            cls.LOG_FILE_FP.write(msg + '\n')


    @classmethod
    def log_info(cls, tag, message):
        """
        This method defines how the logs will be printed for the INFO level.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        It also prints the log in specific color if the "color" argument is True
        Args:
            Tag
            Message
            Color(Optional)
        Returns:
            None
        """
        cls.log(LogLevel.INFO, tag, message)
        

    @classmethod
    def log_verbose(cls, tag, message):
        """
        This method defines how the logs will be printed for the VERBOSE level.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        Args:
            Tag
            Message
        Returns:
            None
        """
        cls.log(LogLevel.VERBOSE, tag, message)


    @classmethod
    def log_error(cls, tag, message):
        """
        This method defines how the logs will be printed for the ERROR level.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        These logs are printed in RED color
        Args:
            Tag
            Message
        Returns:
            None
        """
        cls.log(LogLevel.ERROR, tag, message)


    @classmethod
    def log_warn(cls, tag, message):
        """
        This method defines how the logs will be printed for the WARN level.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        These logs are printed in YELLOW color
        Args:
            Tag
            Message
        Returns:
            None
        """
        cls.log(LogLevel.WARN, tag, message)


    @classmethod
    def log_debug(cls, tag, message):
        """
        This method defines how the logs will be printed for the DEBUG level.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        These logs are printed in CYAN color
        Args:
            Tag
            Message
        Returns:
            True or False
        """
        cls.log(LogLevel.DEBUG, tag, message)


    @classmethod
    def log_critical(cls, tag, message):
        """
        This method defines how the logs will be printed for the CRITICAL level.
        This method prints the log message along with the tag consisting of timestamp, log level and given tag
        These logs are printed in RED color
        Args:
            Tag
            Message
        Returns:
            True or False
        """
        cls.log(LogLevel.CRITICAL, tag, message)


    @classmethod
    def strip_ansi_codes(cls, s):
        """
        Remove the ANSI codes from the string using regex
        Args:
            Message
        Returns:
            Stripped message
        """
        return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)


    @classmethod
    def currentTime(cls, ):
        """
        Gets the current system time
        Args:
            None
        Returns:
            Current time in string format
        """
        return str(datetime.datetime.now().strftime("%m-%d %H:%M:%S:%f"))[:-3]


    @classmethod
    def log_exception(cls, tag=""):
        """
        Prints the exception in RED color along with timestamp, log level and given tag
        Args:
            Tag
        Returns:
            None
        """
        lines = str(traceback.format_exc()).split('\n')
        del lines[-1]
        for line in lines:
            cls.log(LogLevel.ERROR, tag, line)


    @classmethod
    def log_stacktrace(cls, tag=""):
        """
        Prints the stacktrace in RED color along with timestamp, log level and given tag
        Args:
            Tag
        Returns:
            None
        """
        lines = str(''.join(traceback.format_stack())).split('\n')
        del lines[-1]
        for line in lines:
            cls.log(LogLevel.ERROR, tag, line)
