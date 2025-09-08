class Event:
    def __init__(self, name):
        self.name=name

    def __str__(self):
        return self.name 
    

""" Widget is core class of the application. """
class Widget:
    def __init__(self, parent=None):
        self.parent=parent
    
    def handle(self, event):
        """ performs dynamic dispatching through hasattr and getattr to decide who is the handler of the event """

        handler=f"handle_{event}"
        if hasattr(self, handler):
            method=getattr(self, handler)
            method(event)

        elif self.parent is not None:
            self.parent.handle(event)
        
        elif hasattr(self, "handle_default"):
            self.handle_default(event)

"""" Implementing MainWindow, SendDialog and MsgText class"""

class MainWindow(Widget):
    def handle_close(self, event):
        print(f"Main Window: {event}")

    def handle_default(self, event):
        print(f"Main Window Default: {event}")


class SendDialog(Widget):
    def handle_paint(self, event):
        print(f"Send Dialog: {event}")

class MsgText(Widget):
    def handle_down(self, event):
        print(f"Message Dialog: {event}")


""" creating main function """
def main():
    main_window=MainWindow()
    send_dialog=SendDialog()
    message_text=MsgText()

    for e in ("down", "paint", "unhandled", "close"):
        evt = Event(e)
        print (f"Sending event {evt} to Main Window")
        main_window.handle(evt)

        print (f"Sending event {evt} to Send Dialog")
        send_dialog.handle(evt)

        print (f"Sending event {evt} to Message Text")
        message_text.handle(evt)

if __name__=="__main__":
    main()