import ttkbootstrap as tkb 
from ttkbootstrap.dialogs import Messagebox

class GUIBuilder:

    def __init__(self, root):
        self.root=root
        self.row=None 
        self.column=None 

    @property
    def current_row(self):
        return self.row 
    
    @property
    def current_column(self):
        return self.column

    def add_horizontal_separator(self, row=0, column=0, columnspan=0, sticky="ew"):
        self.row, self.column=row, column
        separator=tkb.Separator(self.root)
        separator.grid(row=row, column=column, columnspan=columnspan, sticky=sticky, padx=10, pady=20)
        return separator
    
    def add_label(self, text:str="Default Label", row:int=0, column:int=0, columnspan=1, rowspan=1, sticky="ew"):
        self.row, self.column=row, column 
        label_=tkb.Label(self.root, text=text)
        label_.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=10, pady=10)
        return label_
    
    def add_normal_entry(self, row=0, column=0, columnspan=1, rowspan=1, sticky="ew"):
        self.row, self.column=row, column
        entry_normal=tkb.Entry(self.root)
        entry_normal.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=10, pady=10)
        return entry_normal
    
    def add_password_entry(self, row=0, column=0, columnspan=1, rowspan=1, sticky="ew"):
        self.row, self.column=row, column
        entry_password=tkb.Entry(self.root, show="*")
        entry_password.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=10, pady=10)
        return entry_password
    
    def add_button(self, text="Submit", row=0, column=0, columnspan=1, rowspan=1, sticky="ew"):
        self.row, self.column=row, column 
        button_=tkb.Button(self.root, text=text)
        button_.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=10, pady=10)
        return button_