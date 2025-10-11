""" Forms are something to collect information from the user. All forms are UI but not all UI are forms """

import PyQt6.QtWidgets as qtw 
import PyQt6.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Login")

        # Not using Vertical Box layout
        # self.setLayout(qtw.QVBoxLayout())

        # Create the layout 
        form_layout=qtw.QFormLayout()
        self.setLayout(form_layout)

        # Add widgets - first is the label
        label_1=qtw.QLabel(self, text="This is a Cool Label Row") 

        # add the entry for userid and password; password field being masked! 
        user_id=qtw.QLineEdit(self)
        password=qtw.QLineEdit(self, echoMode=qtw.QLineEdit.EchoMode.Password)

        # add these widgets to form 
        form_layout.addRow(label_1)
        form_layout.addRow("User ID", user_id)
        form_layout.addRow("Password", password)
        form_layout.addRow(qtw.QPushButton("submit", clicked=lambda:press_it()))

        self.show()


        def press_it():
            label_1.setText(f"You pressed the button! {user_id.text()}")

app=qtw.QApplication([])
mw=MainWindow() 
app.exec()
