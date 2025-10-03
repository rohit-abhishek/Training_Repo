"""
Custom exception handling  
"""

import logging 
import traceback 

log_handler = logging.getLogger(__name__)

class ValidationException(Exception):
    """ Validation exception """

    def __init__(self, message):
        self.message = message 
        Exception.__init__(self, self.message)
        log_handler.error(traceback.format_exc())

    def __str__(self):
        log_handler.critical(self.message)
        return repr(self.message)
    

class ProcessingException(Exception):
    """ Process Exception """
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)
        log_handler.error(traceback.format_exc())

    def __str__(self):
        log_handler.critical(self.message)
        return repr(self.message)