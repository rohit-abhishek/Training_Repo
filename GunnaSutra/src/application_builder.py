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
from utility_modules import utilities
from utility_modules.contants import SETUP_CONFIGURATION
from user_interface_modules import SplashScreen, ControlSettings, CustomTopLevel


class ApplicationBuilder(tkb.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set up splash screen for user to wait while performing below operations 
        self.initialize_application()
        print("Back to initialization")


    def initialize_application(self):
        self.splash=SplashScreen(self)

        self.splash.update_initialization_status()

        # get the setup configuration 
        self.splash.update_configuration_status()
        self.configuration_location=utilities.get_system_location(file_name=SETUP_CONFIGURATION)
        self.setup_configuration=utilities.get_setup_configuration(self.configuration_location) 

        # set up workspace
        self.splash.update_workspace_status()
        workspace_location=self.setup_configuration.application_control_data.workspace_location
        application_name=self.setup_configuration.application_control_data.application_name
        self.workpsace_location=utilities.create_workspace(workspace_location, application_name)

        # create logging handles 
        self.splash.update_logging_status()
        self.setup_logging()

        # Apply theme 
        default_theme=self.setup_configuration.application_user_interface.default_theme
        self.style_name=tkb.Style()
        self.theme_names=self.style_name.theme_names() 
        self.theme_names.sort() 
        self.style_name.theme_use(default_theme)            

        # now add the user prompt for user to enter userid and passphrase
        self.splash.update_ready_status()
        self.valid_credentials=False 
        self.authentication=ControlSettings(self.get_user_auth_flag)
        self.splash.root.wait_window()



    def setup_logging(self):

        # get default log level 
        log_level_str=self.setup_configuration.application_control_data.logging_level
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


    def get_user_auth_flag(self, valid_credentials):
        self.valid_credentials=valid_credentials
        if self.valid_credentials:
            self.authentication.close_user_auth_screen()
            self.splash.update_authentication_sucessful()
            self.splash.update_application_window()
        else: 
            self.splash.update_error_status()
        self.splash.close_splash_screen()


    def run(self):
        self.mainloop()


if __name__=="__main__":
    try:
        a=ApplicationBuilder() 
        a.run()
    except Exception as e:
        logging.error(f"Falied to start application: {e}", exc_info=False)