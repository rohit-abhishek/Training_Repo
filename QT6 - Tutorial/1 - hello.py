import PyQt6.QtWidgets as qtw 

# label is part of Widget system but chaging the size of widget is not part of widget system. For that import 
import PyQt6.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # set the window title 
        self.setWindowTitle("Hello World")

        # set the Vertical layout 
        self.setLayout(qtw.QVBoxLayout())

        # create a label 
        my_label=qtw.QLabel("Hello, What's your name?: ", self)

        # change the font size of the label 
        my_label.setFont(qtg.QFont("Helvetica", 18))

        # put the label on the screen 
        self.layout().addWidget(my_label)

        # add entry box to enter the name 
        my_entry=qtw.QLineEdit(self)
        my_entry.setObjectName("name_field")
        my_entry.setText("")
        self.layout().addWidget(my_entry)

        # Let's create a button
        my_button=qtw.QPushButton("Press Me!", self, clicked=lambda:press_it())
        self.layout().addWidget(my_button)

        # always use show method to show the app 
        self.show() 

        def press_it(): 
            # add name to the label 
            my_label.setText(f"Hello {my_entry.text()}")

            # clear the entry box 
            my_entry.setText("")


app=qtw.QApplication([])
mw=MainWindow() 

# run the app 
app.exec()