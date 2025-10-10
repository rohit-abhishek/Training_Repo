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
        my_label=qtw.QLabel(parent=self, text="Hello, What's your name?: ")

        # change the font size of the label 
        my_label.setFont(qtg.QFont("Helvetica", 24))

        # put the label on the screen 
        self.layout().addWidget(my_label)

        # Add a spinbox (NOTE - if you press enter at 56 and then increment; it will increment to 61 because increment set is of 5)
        my_spin=qtw.QSpinBox(self, value=10, maximum=100, minimum=0, singleStep=5, prefix="#", suffix=" Selected")

        # to add flaoting numbers to spin box you need to define 
        my_spin_double=qtw.QDoubleSpinBox(self, value=0.1, maximum=1, minimum=0, singleStep=0.1, prefix="Probablity ")

        # Change font size of the spin box 
        my_spin.setFont(qtg.QFont("Helvetica", 18))
        my_spin_double.setFont(qtg.QFont("Helvetica", 18))

        self.layout().addWidget(my_spin)
        self.layout().addWidget(my_spin_double)

        # Let's create a button
        my_button=qtw.QPushButton(parent=self, text="Press Me!", clicked=lambda:press_it())
        self.layout().addWidget(my_button)

        # always use show method to show the app 
        self.show() 

        def press_it(): 
            # add name to the label 
            my_label.setText(f"You picked: {my_spin.value()} Probablity: {my_spin_double.value()}")


app=qtw.QApplication([])
mw=MainWindow() 

# run the app 
app.exec()