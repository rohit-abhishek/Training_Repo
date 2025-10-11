import sys
import time
import logging
from enum import Enum

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame
)

class StatusMessage(Enum):
    INITIALIZATION = "Initializing..."
    CONFIGURATION = "Configuring..."
    WORKSPACE = "Setting up workspace..."
    LOGGING = "Starting logging..."
    READY = "Application is ready!"
    SUCCESSFUL = "Authentication successful!"
    MAIN = "Launching main window..."
    ERROR = "An error occurred!"


class SplashScreen(QMainWindow):
    def __init__(self, wait_time=1):
        super().__init__()

        self.wait_time = wait_time
        self.ready = False

        self.setWindowTitle("GunnaSutra")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        self.center_window()
        self.setup_ui()

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.title_label = QLabel("Gunnsutra Application")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(self.title_label)      

        self.gif_frame = QFrame()
        gif_layout = QVBoxLayout(self.gif_frame)
        gif_layout.setContentsMargins(0, 0, 0, 0)
        gif_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.gif_frame)

        self.loading_label = QLabel("●●●")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gif_layout.addWidget(self.loading_label)

        self.status_label = QLabel(StatusMessage.INITIALIZATION.value)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(self.status_label)

        self.dots = ["●", "●●", "●●●", "●●●●", "●●●●●"]
        self.dot_index = 0

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
        # time.sleep(self.wait_time)

    def update_configuration_status(self):
        self.update_status(StatusMessage.CONFIGURATION.value)
        # time.sleep(self.wait_time)

    def update_workspace_status(self):
        self.update_status(StatusMessage.WORKSPACE.value)
        # time.sleep(self.wait_time)

    def update_logging_status(self):
        self.update_status(StatusMessage.LOGGING.value)
        # time.sleep(self.wait_time)

    def update_ready_status(self):
        self.update_status(StatusMessage.READY.value)
        self.ready = True
        # time.sleep(self.wait_time)

    def update_authentication_successful(self):
        self.update_status(StatusMessage.SUCCESSFUL.value)
        # time.sleep(self.wait_time)

    def update_application_window(self):
        self.update_status(StatusMessage.MAIN.value)
        # time.sleep(self.wait_time)

    def update_error_status(self):
        self.update_status(StatusMessage.ERROR.value)
        # time.sleep(self.wait_time)

    def close_splash_screen(self):
        self.animation_timer.stop()
        self.close()


def main():
    app = QApplication(sys.argv)

    try:
        splash = SplashScreen(wait_time=1)
        splash.show()

        # Simulate initialization steps (this would usually be in a thread or async)
        splash.update_initialization_status()
        splash.update_configuration_status()
        splash.update_workspace_status()
        splash.update_logging_status()
        splash.update_ready_status()
        splash.update_authentication_successful()
        splash.update_application_window()

        splash.close_splash_screen()

    except Exception as e:
        logging.error(f"Failed to start application: {e}", exc_info=True)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
