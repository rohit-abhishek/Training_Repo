import ttkbootstrap as tkb 
import sys

class CustomTopLevel(tkb.Toplevel):
    def __init__(self, title="ttkbootstrap", iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, transient=None, overrideredirect=False, windowtype=None, topmost=False, toolwindow=False, alpha=1, **kwargs):
        super().__init__(title, iconphoto, size, position, minsize, maxsize, resizable, transient, overrideredirect, windowtype, topmost, toolwindow, alpha, **kwargs)
        self.title=title 
        self.x, self.y=None, None 
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.exit_application)

    def center_window(self):
        self.update_idletasks()
        width=self.winfo_width()
        height=self.winfo_height()
        self.x=(self.winfo_screenwidth() // 2) - (width // 2)
        self.y=(self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{self.x}+{self.y}")

    def exit_application(self):
        self.update()
        self.destroy()
        sys.exit()        