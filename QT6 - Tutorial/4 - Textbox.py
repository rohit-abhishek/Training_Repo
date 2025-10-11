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
        my_text=qtw.QTextEdit(self, 
                              acceptRichText=True, 
                              lineWrapMode=qtw.QTextEdit.LineWrapMode.FixedColumnWidth, 
                              lineWrapColumnOrWidth=50,             # Number of characters in single line for wrapping the text
                              placeholderText="Hello World!",       # Goes away as soon as you start typing
                            #   plainText="This is real text",      # Real text. Does not go away 
                              html="<h1> this is header block </h1>",       # You can insert html as well to text box
                              readOnly=False)
        self.layout().addWidget(my_text)

        # Let's create a button
        my_button=qtw.QPushButton(parent=self, text="Press Me!", clicked=lambda:press_it())
        self.layout().addWidget(my_button)

        # always use show method to show the app 
        self.show() 

        def press_it(): 
            # add name to the label 
            my_label.setText(f"You Typed: {my_text.toPlainText()}")
            my_text.setPlainText(f"You Pressed the Button")

app=qtw.QApplication([])
mw=MainWindow() 

# run the app 
app.exec()