"""
Module for the splash screen using Qt6.
This module provides a splash screen implementation using PyQt6. 
It displays a loading animation and status messages during application initialization.
It expose some of the method to update the status message on real time basis.
"""

import sys
import time
from enum import Enum
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame, QStyle
from PyQt6.QtGui import QFont
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

    # def get_screen_resolution(self) -> list[int, int]:
    #     app = QApplication.instance()
    #     if app is None:
    #         app = QApplication(sys.argv)
    #     screen = app.primaryScreen()
    #     size = screen.size()
    #     return size.width(), size.height()
    
    def get_best_fit(self, width_ratio=0.5, height_ratio=0.5) -> list[int, int]:
        return int(self.screen_width * width_ratio), int(self.screen_height * height_ratio)


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

        # Set the window properties 
        self.setWindowTitle("GunnaSutra")
        self.setFixedSize(window_width, window_height)
        
        # ensure window is frameless and always on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
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

        self.title_label=QLabel("Gunnasutra Application")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # self.title_label_style=QStyle()


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