""" This program authenticates the user entered credentials and returns authentication success flag"""

import os, sys
import ttkbootstrap as tkb 
import logging 
from ttkbootstrap.dialogs import Messagebox
from authorization_modules import AuthToken
from exception_modules import CustomException, ApplicationInterrput
from utility_modules import utilities
from utility_modules.contants import SALT_FILE_NAME, SECRET_FILE_NAME, MESSAGE_LOOKUP
from utility_modules.gui_builder import GUIBuilder
from .custom_widgets import CustomTopLevel

logger=logging.getLogger(__name__)

class ControlSettings:
    """ GUI Handler for Control Settings - prompts for user to enter passphrase """

    def __init__(self, user_auth_flag_func):
        self.__secret_message=None 
        self.__salt_data=None
        self.user_auth_flag_func=user_auth_flag_func 
        self.valid_secret_message=False
        self.get_secret_salt_data() 
        self.initialize_gui()

    def get_secret_salt_data(self):
        """ """
        # validate if key are present in the desired location 
        salt_file_location=utilities.get_system_location(file_name=SALT_FILE_NAME)
        secret_message_location=utilities.get_system_location(file_name=SECRET_FILE_NAME)
        
        # get the values 
        try:
            with open(salt_file_location, "r") as fp:
                self.__salt_data=fp.readlines()[0]
            with open(secret_message_location, "r") as fp:
                self.__secret_message=fp.readlines()[0]

        except:
            message_key="ERRMSG001"
            self.raise_custom_error(message_key)

        if not self.__secret_message:
            message_key="ERRMSG002"
            self.raise_custom_error(message_key)
            
        if not self.__salt_data:
            message_key="ERRMSG003"
            self.raise_custom_error(message_key)
            

    def initialize_gui(self):
        self.root=CustomTopLevel("GunnaSutra Login")
        self.root.protocol("WM_DELETE_WINDOW", self.root.exit_application)
        self.main_frame=tkb.Frame(self.root)
        self.main_frame.pack(side="top", expand=True, fill="both")
        self.create_user_prompt_window()
    

    def create_user_prompt_window(self):

        # add a separator 
        builder=GUIBuilder(self.main_frame)
        # separator=builder.add_horizontal_separator(row=0, column=0, columnspan=3, sticky="ew")

        # add user id label and entry 
        user_id_label=builder.add_label(text="User ID", row=1, column=0, sticky="w")
        self.user_id_entry=builder.add_normal_entry(row=1, column=1, columnspan=2, sticky="ew")

        # add password label and entry 
        user_passphrase_label=builder.add_label(text="User Passphrase", row=2, column=0, sticky="w")
        self.user_passphrase_entry=builder.add_password_entry(row=2, column=1, columnspan=2, sticky="ew")

        # add a separator 
        separator=builder.add_horizontal_separator(row=3, column=0, columnspan=3, sticky="ew")

        # add submit button 
        self.user_passphrase_submit=builder.add_button(text="Submit", row=4, column=0, sticky="w")
        self.user_passphrase_submit.configure(command=lambda:self.validate_user_authorization(self.user_id_entry, self.user_passphrase_entry))

        # add cancel button 
        self.user_passphrase_submit=builder.add_button(text="Cancel", row=4, column=2, sticky="e")
        self.user_passphrase_submit.configure(command=lambda:self.root.exit_application())


    def raise_custom_error(self, message_key):
        message_text=MESSAGE_LOOKUP.get(message_key)
        raise CustomException(message_key, message_text)


    def handle_custom_exception(self, cx:CustomException):
        if logger.isEnabledFor(logging.DEBUG):
            logger.error(f"Custom Exception occured: {cx}", exc_info=True)
        else:
            logger.error(f"Custom Exception occured: {str(cx)}", exc_info=False)
        Messagebox.show_error(message=cx.message_text, title="GunnSutra Exception", parent=self.root)


    def handle_application_interrupt(self, cx:ApplicationInterrput):
        if logger.isEnabledFor(logging.DEBUG):
            logger.error(f"Custom Exception occured: {cx}", exc_info=True)
        else:
            logger.error(f"Custom Exception occured: {str(cx)}", exc_info=False)
        Messagebox.show_error(message=f"{cx.message_text}", title="GunnSutra Error", parent=self.root)
        sys.exit()


    def handle_general_exception(self, e:Exception, message_key:str):
        message_text=MESSAGE_LOOKUP.get(message_key)

        if logger.isEnabledFor(logging.DEBUG):
            logger.error(f"Exception occured: {message_key} & Error Message: {e}", exc_info=True)
        else:
            logger.error(f"Exception occured: {message_key} & Error Message: {e}", exc_info=False)
        Messagebox.show_error(message=message_text, title="GunnSutra Error", parent=self.root)


    def validate_empty_field(self, field_value, message_key):
        if field_value is None or field_value == "":
            self.raise_custom_error(message_key)
        return field_value.strip()


    def validate_user_authorization(self, user_id_widget, passphrase_widget):
        user_id=user_id_widget.get() 
        passphrase=passphrase_widget.get() 
            
        try:
            user_id=self.validate_empty_field(user_id, "ERRMSG011")
            passphrase=self.validate_empty_field(passphrase, "ERRMSG012") 

            # generate key and validate secret message
            auth_object=AuthToken()
            passphrase_bytes=auth_object.string_to_bytes(passphrase)
            salt_bytes=auth_object.hexstring_to_bytes(self.__salt_data)
            secret_message_encoded_bytes=auth_object.string_to_bytes(self.__secret_message)

            # get the key 
            key_bytes=auth_object.get_key_from_passphrase_and_salt(passphrase_bytes, salt_bytes)
            secret_message=auth_object.decrypt_secret_message(key_bytes, secret_message_encoded_bytes)

            # validate the data in secret message
            self.valid_secret_message=auth_object.validate_secret_message(user_id, secret_message)
            self.user_auth_flag_func(self.valid_secret_message)
                
        except CustomException as cx: 
            self.handle_custom_exception(cx)

        except ApplicationInterrput as ax:
            self.handle_application_interrupt(ax)
            
        except Exception as e:
            message_key="ERRMSG010"
            self.handle_general_exception(e, message_key)
    
    def close_user_auth_screen(self):
        self.root.update()
        self.root.destroy()

        
    def run(self):
        logger.info("Starting application main loop")
        self.root.mainloop()


def main():  

    try:
        app=ControlSettings()
        app.run()
    except Exception as e:
        logging.error(f"Falied to start application: {e}", exc_info=False)


if __name__=="__main__":
    main()
