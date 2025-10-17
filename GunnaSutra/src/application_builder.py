""" 
This is launch program which will create the Splash screen. 
This program will load the system configurations - Features that cannot be modified by the user using GUI. 
Any change system_configuration.yaml file will require application restart for loading the changes. 
It will then pass control to ControlSettings for user to enter user id and password. Control Settings will perform 
Cryptography authentication and authorization for the user. 
"""

import sys, os
import logging
import time 
import ttkbootstrap as tkb
from utility_modules.utilities import FileLocator, Workspace, SetupConfig
from utility_modules.contants import SETUP_CONFIGURATION
from user_interface_modules import SplashScreen, UserCredentials
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


class ApplicationBuilder():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # first off create splash screen for user to see the progress 
        self.splash=SplashScreen()
        self.splash.show()

        # initialize the splash screen 
        self.initialize_splash_screen()

        # get the application configurations 
        self.get_configurations()

        # set up application workspace 
        self.create_workspace()

        # create logging handles 
        self.create_logging_handles()

        # prompt user to enter credentials 
        self.enter_login_credentials()


    def initialize_splash_screen(self):
        # Show intialization message
        self.splash.update_initialization_status()


    def get_configurations(self):

        # update splash screen message
        self.splash.update_configuration_status()

        config_locator=FileLocator(SETUP_CONFIGURATION)
        self.config_location=config_locator.get_system_location()
        
        # load the configurations 
        setup_config_object=SetupConfig(self.config_location)
        self.config_data=setup_config_object.get_configuration_data()


    def create_workspace(self):
        self.splash.update_workspace_status()

        # get workspace location and application name 
        workspace_directory=self.config_data.application_control_data.workspace_location 
        application_name=self.config_data.application_control_data.application_name

        # create workspace object 
        self.workspace_object=Workspace(workspace_directory, application_name)
        self.workpsace_location=self.workspace_object.get_workspace_location()


    def create_logging_handles(self):
        self.splash.update_logging_status()

        log_level_str=self.config_data.application_control_data.logging_level
        log_level=logging._nameToLevel.get(log_level_str, 0)

        logging.basicConfig(
            level=log_level,
            format=" %(asctime)s - {%(name)s : %(lineno)d} - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(self.workpsace_location, "GunnSutra.log"), mode="w")
            ]
        )
        self.logger=logging.getLogger(__name__)
        self.logger.info("Application Initialized")
        if log_level != logging.DEBUG: 
            sys.tracebacklimit=0
        

    def enter_login_credentials(self):
        self.splash.update_ready_status()

        # bring up login screen for user to enter credentials 
        self.user_login=UserCredentials(self)
        self.user_login.show()
        self.user_login.raise_() 
        self.user_login.activateWindow()
        


    def get_user_auth_flag(self, valid_credentials):
        self.valid_credentials=valid_credentials
        if self.valid_credentials:
            self.authentication.close_user_auth_screen()
            self.splash.update_authentication_sucessful()
            self.splash.update_application_window()
        else: 
            self.splash.update_error_status()
        self.splash.close_splash_screen()



if __name__=="__main__":
    app=QApplication(sys.argv)

    try:
        gunnasutra=ApplicationBuilder() 
    except Exception as e:
        logging.error(f"Falied to start application: {e}", exc_info=False)

    sys.exit(app.exec())