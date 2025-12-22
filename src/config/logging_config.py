import logging
import sys
from enum import Enum

__all__ = ['LoggingConfig']

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        res = not any(word in record.getMessage().lower() for word in ['password', 'token', 'secret'])
        return res

class OutputLogging(Enum):
    file = 'file'
    console = 'console'

class LoggingConfig:
    def __init__(self, level=logging.INFO, name='test', formatter='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter(fmt=formatter)

    def create_handler(self, output_logging: OutputLogging, file='test.log', file_mode='a', formatter=None, level=None):
        handler = None
        match output_logging:
            case output_logging.file:
                handler = logging.FileHandler(filename=file, mode=file_mode)
            case output_logging.console:
                handler = logging.StreamHandler()
        if level:
            handler.setLevel(level)
        if formatter:
            handler.setFormatter(formatter)
        else:
            handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def create_filter_for_handler(self, filter):
        self.logger.addFilter(filter())