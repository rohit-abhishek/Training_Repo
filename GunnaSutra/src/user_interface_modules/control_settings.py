import sys 
import logging 
from authorization_modules import AuthToken
from exception_modules import CustomException, ApplicationInterrput
from utility_modules.utilities import FileLocator
from utility_modules.contants import UI_MODULE_LOOKUP, MESSAGE_LOOKUP

from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox, QDialogButtonBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import uic 
from PyQt6.QtCore import QDate

# get the log handle if exists 
logger=logging.getLogger(__name__)

class UserCredentials(QDialog):
    def __init__(self, root):
        super().__init__()

        self.root=root
        # Get UI Raw files 
        self.raw_ui_location=FileLocator(UI_MODULE_LOOKUP.get("user_login", None)).get_system_location()
        if not self.raw_ui_location:
            logger.exception(MESSAGE_LOOKUP.get("ERRMSG015"))
            self.exit_application()

        # load GUI File 
        uic.loadUi(self.raw_ui_location, self)

        # set the window title 
        # self.setWindowTitle("Gunnasutra Login")

        # get the widgets for User Login screen 
        self.get_child_widgets() 

        # create button commands 
        self.create_button_commands()

    
    def get_child_widgets(self):
        self.user_name_edit=self.findChild(QLineEdit, "userName")
        self.passphrase_edit=self.findChild(QLineEdit, "passphrase")
        self.button_box=self.findChild(QDialogButtonBox, "buttonBox")

    def create_button_commands(self):
        self.button_box.accepted.connect(self.validate_user_authorization)
        self.button_box.rejected.connect(self.exit_application)

    def validate_user_authorization(self):
        self.user_name=self.user_name_edit.text()
        self.passphrase=self.passphrase_edit.text()
        self.user_name=self.validate_empty_field(self.user_name, "ERRMSG011")
        self.passphrase=self.validate_empty_field(self.passphrase, "ERRMSG012")

        # Validate the user credentials 
        auth_object=AuthToken(self.user_name, self.passphrase)

        if not auth_object.validate_auth_token():
            message_key="ERRMSG016"
            self.raise_custom_error(message_key)


    def validate_empty_field(self, field_value:str, message_key:str):
        if field_value is None or field_value == "":
            self.raise_custom_error(message_key)
        return field_value.strip()        
    
    def raise_custom_error(self, message_key):
        message_text=MESSAGE_LOOKUP.get(message_key)
        raise CustomException(message_key, message_text)
    
    def exit_application(self):
        sys.exit()