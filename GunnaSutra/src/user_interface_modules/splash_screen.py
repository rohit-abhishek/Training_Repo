"""
Module for the splash screen using Qt6.
This module provides a splash screen implementation using PyQt6. 
It displays a loading animation and status messages during application initialization.
It expose some of the method to update the status message on real time basis.
"""

import sys
import time
from enum import Enum
from PyQt6.QtCore import Qt, QTimer, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame, QStyle
from PyQt6.QtGui import QFont

# Change below imports for standalone call
from utility_modules.contants import QSS_1K_FILE, QSS_2K_FILE, QSS_3K_FILE, QSS_4K_FILE
from utility_modules.utilities import FileLocator
import logging

class StatusMessage(Enum):
    """ Message for splash screen status updates """

    INITIALIZATION = "Initializing Application..."
    CONFIGURATION = "Loading Configuration..."
    WORKSPACE = "Setting up Workspace..."
    LOGGING = "Configuring Logging..."
    READY = "Application is Ready."
    SUCCESSFUL = "Authentication Successful."
    MAIN = "Launching Main Application..."
    ERROR = "An Error Occurred..."


class ScreenManager: 
    """ Checks the screen resolution and provides methods to get the best fit for application windows """

    def __init__(self):
        self.manager=QApplication.instance()
        if self.manager is None:
            self.manager = QApplication(sys.argv)
      
        self.screen = self.manager.primaryScreen()
        self.size = self.screen.size()

        # screen width and height 
        self.screen_width = self.size.width() 
        self.screen_height = self.size.height()

        # print(self.screen_width, self.screen_height)

    def get_best_fit(self, width_ratio=0.5, height_ratio=0.5) -> list[int, int]:
        return int(self.screen_width * width_ratio), int(self.screen_height * height_ratio)
    
    def get_style_sheet(self):
        if self.screen_width <= 1280:
            self.style_sheet_file=FileLocator(QSS_1K_FILE).get_system_location()
        elif self.screen_width <= 1920 and self.screen_width > 1280:
            self.style_sheet_file=FileLocator(QSS_2K_FILE).get_system_location()
        elif self.screen_width <= 2560 and self.screen_width > 1920:
            self.style_sheet_file=FileLocator(QSS_3K_FILE).get_system_location()
        elif self.screen_width <= 3840 and self.screen_width > 2560:
            self.style_sheet_file=FileLocator(QSS_4K_FILE).get_system_location()
        return self.style_sheet_file

    
class SplashScreen(QMainWindow):
    """ Create startup splash screen for the application """

    def __init__(self, wait_time=1): 
        """ Initialize the splash screen """

        super().__init__()
        self.wait_time=wait_time
        self.ready=False 

        # get the screen manager object 
        self.screen_manager=ScreenManager()
        window_width, window_height=self.screen_manager.get_best_fit(0.20, 0.15)

        # get the qss file and apply the style
        self.qss_file=self.screen_manager.get_style_sheet()
        with open(self.qss_file, "r") as fp:
            self.style_data=fp.read()
            self.setStyleSheet(self.style_data)
            # print(self.style_data)

        # Set the window properties 
        self.setWindowTitle("GunnaSutra")
        self.setFixedSize(window_width, window_height)
        
        # ensure window is frameless and always on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # cetner the window and set up the GUI
        self.center_window()
        self.setup_gui()


    def center_window(self):
        """ Center the window on the screen """
        # the screen dimesions
        screen=QApplication.primaryScreen().availableGeometry() 

        # calculate the x and y coordinates to center the window
        x=(screen.width() - self.width()) // 2
        y=(screen.height() - self.height()) // 2

        # move the window to x and y coordinates
        self.move(x, y)


    def setup_gui(self):
        """ Set up Splash screen GUI components """

        # create a widget and set to center 
        central_widget=QWidget() 
        self.setCentralWidget(central_widget)

        # Create a Vertical box layout
        layout=QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Add the title label 
        self.title_label=QLabel("Gunnasutra Application")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.title_label)

        # Add frames 
        self.gif_frame = QFrame()
        gif_layout = QVBoxLayout(self.gif_frame)
        gif_layout.setContentsMargins(0, 0, 0, 0)
        gif_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.gif_frame)

        # Add animation label 
        self.loading_label = QLabel("●●●")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gif_layout.addWidget(self.loading_label)

        # Add Status message 
        self.status_label = QLabel(StatusMessage.INITIALIZATION.value)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(self.status_label)

        # Define dots to be loaded 
        self.dots = ["●", "●●", "●●●", "●●●●", "●●●●●"]
        self.dot_index = 0

        # add animation timer 
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_loading)
        self.animation_timer.start(200)

    def animate_loading(self):
        self.loading_label.setText(self.dots[self.dot_index])
        self.dot_index = (self.dot_index + 1) % len(self.dots)

    def update_status(self, message: str):
        self.status_label.setText(message)
        QApplication.processEvents()

    def update_initialization_status(self):
        self.update_status(StatusMessage.INITIALIZATION.value)
        QThread.sleep(self.wait_time)

    def update_configuration_status(self):
        self.update_status(StatusMessage.CONFIGURATION.value)
        QThread.sleep(self.wait_time)

    def update_workspace_status(self):
        self.update_status(StatusMessage.WORKSPACE.value)
        QThread.sleep(self.wait_time)

    def update_logging_status(self):
        self.update_status(StatusMessage.LOGGING.value)
        QThread.sleep(self.wait_time)

    def update_ready_status(self):
        self.update_status(StatusMessage.READY.value)
        self.ready = True
        QThread.sleep(self.wait_time)

    def update_authentication_successful(self):
        self.update_status(StatusMessage.SUCCESSFUL.value)
        QThread.sleep(self.wait_time)

    def update_application_window(self):
        self.update_status(StatusMessage.MAIN.value)
        QThread.sleep(self.wait_time)

    def update_error_status(self):
        self.update_status(StatusMessage.ERROR.value)
        QThread.sleep(self.wait_time)

    def close_splash_screen(self):
        self.animation_timer.stop()
        self.close()


def main():
    app = QApplication(sys.argv)

    try:
        splash = SplashScreen(wait_time=1)
        splash.show()

        # Simulate initialization steps (this would usually be in a thread or async)


    except Exception as e:
        logging.error(f"Failed to start application: {e}", exc_info=True)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()