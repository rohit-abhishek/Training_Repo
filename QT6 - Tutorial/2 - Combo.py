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
        my_label.setFont(qtg.QFont("Helvetica", 18))

        # put the label on the screen 
        self.layout().addWidget(my_label)

        # add combo box (editable=True will make the combo editable. Click enter to add the new item to the combobox)
        my_combo=qtw.QComboBox(self, editable=True, insertPolicy=qtw.QComboBox.InsertPolicy.InsertAtTop)

        # Add items to the combo box 
        my_combo.addItem("Pepperoni", "Something")
        my_combo.addItem("Cheese", 2)
        my_combo.addItem("Pepper", qtw.QWidget)
        my_combo.addItem("Mushroom")
        my_combo.addItem("Paneer")

        # You can add items in single shot 
        my_combo.addItems(["One", "Two", "Three"])

        # You can use insertItems as well by telling which position in the combolist 
        my_combo.insertItem(2, "Third thing")

        self.layout().addWidget(my_combo)

        # Let's create a button
        my_button=qtw.QPushButton(parent=self, text="Press Me!", clicked=lambda:press_it())
        self.layout().addWidget(my_button)

        # always use show method to show the app 
        self.show() 

        def press_it(): 
            # add name to the label 
            my_label.setText(f"You picked Text: {my_combo.currentText()} Data: {my_combo.currentData()} Index: {my_combo.currentIndex()}")


app=qtw.QApplication([])
mw=MainWindow() 

# run the app 
app.exec()