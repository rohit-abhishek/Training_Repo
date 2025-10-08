import ttkbootstrap as tkb 
import logging 
from enum import Enum 
import time 

class StatusMessage(Enum):
    INITIALIZATION="Initializing Application..."
    CONFIGURATION="Getting Application Setup Configuration..."
    WORKSPACE="Creating User Workspace..."
    LOGGING="Enabling Application Logging..."
    READY="Bringing up Gunnasutra Login Screen..."
    SUCCESSFUL="Authentication Successful"
    ERROR="Error Occurred in Getting Setup Configuration..."
    MAIN="Creating Application Window..."


class SplashScreen:
    def __init__(self, parent, wait_time=1):
        self.wait_time=wait_time
        self.parent=parent
        self.parent.withdraw()
        self.root=tkb.Toplevel() 
        self.root.title("GunnaSutra")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.ready=False
        
        self.center_window()
        self.setup_ui() 

    def center_window(self):
        self.root.update_idletasks()
        width=self.root.winfo_width()
        height=self.root.winfo_height() 
        x=(self.root.winfo_screenwidth() // 2) - (width // 2)
        y=(self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

    def setup_ui(self):
        self.main_frame=tkb.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.title_label=tkb.Label(self.main_frame, text="Gunnsutra Application", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(20, 30))

        self.gif_frame=tkb.Frame(self.main_frame)
        self.gif_frame.pack(pady=20)
        self.gif_frame.pack_propagate(True)

        self.loading_label=tkb.Label(self.gif_frame, text="●●●")
        self.loading_label.pack(expand=True)

        self.status_label=tkb.Label(self.main_frame, text=StatusMessage.INITIALIZATION.value, font=("Arial", 12))
        self.status_label.pack(pady=20)

        self.animate_loading()

    def animate_loading(self):
        dots=["●", "●●", "●●●", "●●●●", "●●●●●"]
        current_dots=dots[int(time.time() * 1) % len(dots)]
        self.loading_label.config(text=current_dots)
        if self.root and not self.ready:
            self.after_id=self.root.after(200, self.animate_loading)
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks() 
        self.root.update() 
    
    def update_initialization_status(self):
        self.update_status(StatusMessage.INITIALIZATION.value)
        time.sleep(self.wait_time)

    def update_configuration_status(self):
        self.update_status(StatusMessage.CONFIGURATION.value)
        time.sleep(self.wait_time)

    def update_workspace_status(self):
        self.update_status(StatusMessage.WORKSPACE.value)
        time.sleep(self.wait_time)

    def update_logging_status(self):
        self.update_status(StatusMessage.LOGGING.value)
        time.sleep(self.wait_time)
    
    def update_ready_status(self):
        self.update_status(StatusMessage.READY.value)
        self.ready=True
        time.sleep(self.wait_time)

    def update_authentication_sucessful(self):
        self.update_status(StatusMessage.SUCCESSFUL.value)        
        time.sleep(self.wait_time)

    def update_application_window(self):
        self.update_status(StatusMessage.MAIN.value)
        time.sleep(self.wait_time)

    def update_error_status(self):
        self.update_status(StatusMessage.ERROR.value)
        time.sleep(self.wait_time)

    def close_splash_screen(self):
        self.root.after_cancel(self.after_id)
        self.root.update_idletasks()
        self.root.update()
        self.root.destroy()
        del self.root 
        

    def run(self):
        self.root.mainloop() 

def main():  

    try:
        app=SplashScreen()
        app.run()
    except Exception as e:
        logging.error(f"Falied to start application: {e}", exc_info=False)


if __name__=="__main__":
    main()
