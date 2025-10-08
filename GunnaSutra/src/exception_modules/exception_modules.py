"""
Custom exception handling  
"""
import sys
from utility_modules import MESSAGE_LOOKUP
import logging 

logger=logging.getLogger(__name__)

class CustomException(Exception):
    """ Process Exception """
    def __init__(self, message_key, message_text):
        self.message_key=message_key
        self.message_text=message_text 
        super().__init__(f"{self.message_key} : {self.message_text}")
        logger.error(str(self))

    def __str__(self):
        return f"{self.message_key} : {self.message_text}"
    
class ApplicationInterrput(Exception):
    """ Process Exception """
    def __init__(self, message_key, message_text):
        self.message_key=message_key
        self.message_text=message_text + "Exiting Application"
        super().__init__(f"{self.message_key} : {self.message_text}")
        logger.error(str(self))

    def __str__(self):
        return f"{self.message_key} : {self.message_text}"    


def custom_report_callback_exception(root, exc_type, exc_value, exc_traceback):
    pass 
    # """Handle all uncaught Tkinter exceptions here."""
    # if issubclass(exc_type, CustomException):
    #     if log_handler.isEnabledFor(logging.DEBUG):
    #         # Debug mode: print full traceback
    #         log_handler.error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    #     else:
    #         # Production mode: suppress traceback, show only message
    #         sys.tracebacklimit=0
    #         log_handler.error(str(exc_value))
    # else:
    #     # Fallback: for other exceptions, you may still want full traceback
    #     log_handler.error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

