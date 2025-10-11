""" This module leverages PYQT6 module for Key Generation """

from datetime import datetime, date
import sys, os 
import sqlcipher3
import getpass 

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextEdit, QRadioButton, QStatusBar, QDateEdit, QTableView, QMessageBox, QHeaderView
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import uic 
from PyQt6.QtCore import QDate
from utilities import utility
from utilities.utility import AdminDatabase, AdminRecord, AdminSqlBuilder
from exception_modules import ValidationException
from control_modules import AuthToken


class KeyGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.raw_ui_Location=utility.get_system_location("key_generator.ui")
        if not self.raw_ui_Location:
            print("Raw UI File not found. terminating...")
            sys.exit()

        # load the ui file 
        uic.loadUi(self.raw_ui_Location, self)

        # get all the child widgets
        self.get_child_widgets()

        # default some values
        self.default_child_values()

        # set commands for buttons 
        self.create_button_commands()

        self.show()


    def get_child_widgets(self):

        # get the radiobutton 
        self.radioButton_sqlite_radio=self.findChild(QRadioButton, "databaseOption_sqlite")
        self.radioButton_mysql_radio=self.findChild(QRadioButton, "databaseOption_mysql")

        # get connection string widget 
        self.connectionString_text=self.findChild(QTextEdit, "connectionString")
        
        # get admin password 
        self.adminPassword_line=self.findChild(QLineEdit, "adminPassword")

        # get user id and role 
        self.userId_line=self.findChild(QLineEdit, "userId")
        self.userRole_line=self.findChild(QLineEdit, "userRole")

        # get the start and end dates 
        self.startDate_date=self.findChild(QDateEdit, "startDate")
        self.endDate_date=self.findChild(QDateEdit, "endDate")

        # get the user passphrase 
        self.userPassphrase_line=self.findChild(QLineEdit, "userPassphrase")

        # get the secret message
        self.secretMessage_text=self.findChild(QTextEdit, "secretMessage")
        self.saltMessage_line=self.findChild(QLineEdit, "saltMessage")

        # get the write button 
        self.writeToFile_button=self.findChild(QPushButton, "writeToFile")
        self.getTokenData_button=self.findChild(QPushButton, "getTokenData")
        self.generateTokenData_button=self.findChild(QPushButton, "generateTokenData")
        self.clearForm_button=self.findChild(QPushButton, "clearForm")

        # get the table view and status message widgets as well 
        self.tableView_result_table=self.findChild(QTableView, "tableView")

        # create model for table view 
        self.tableView_result_model=QStandardItemModel()

        # status message widget 
        self.statusbar_status=self.findChild(QStatusBar, "statusbar")


    def default_child_values(self):
        # set sqlite3 radio button default
        self.radioButton_sqlite_radio.setChecked(True)

        # set current date for start and end date 
        self.startDate_date.setDate(QDate.currentDate())
        self.endDate_date.setDate(QDate.currentDate())
        self.reset_gui_data()
        self.statusbar_status.showMessage("Ready!")


    def reset_gui_data(self):

        # set editable
        self.secretMessage_text.setReadOnly(False)
        self.saltMessage_line.setReadOnly(False)      
        
        # remove data 
        self.secretMessage_text.clear()
        self.saltMessage_line.clear()

        # set back to ready only
        self.secretMessage_text.setReadOnly(True)
        self.saltMessage_line.setReadOnly(True)

        # disable write button
        self.writeToFile_button.setEnabled(False)

        # remove items from tableview
        self.initialize_tableview_model()


    def populate_gui(self, user_details:AdminRecord):

        # Set secret message
        self.secretMessage_text.setReadOnly(False)
        self.secretMessage_text.setText(user_details.get_byte_to_string_format(user_details.secret_message))
        self.secretMessage_text.setReadOnly(True)

        # set salt message
        self.saltMessage_line.setReadOnly(False)
        self.saltMessage_line.setText(user_details.salt.hex())
        self.saltMessage_line.setReadOnly(True)

        # set date fields 
        self.startDate_date.setDate(user_details.start_date)
        self.endDate_date.setDate(user_details.end_date)

        # set write to file enabled 
        self.writeToFile_button.setEnabled(True)


    def create_button_commands(self):
        self.getTokenData_button.clicked.connect(self.get_token_data)
        self.generateTokenData_button.clicked.connect(self.generate_token_data)
        self.clearForm_button.clicked.connect(self.reset_gui_data)
        self.writeToFile_button.clicked.connect(self.write_secret_message_salt_string)


    def write_secret_message_salt_string(self):
        try:
            self.statusbar_status.showMessage("Collecting Data")
            user_id=self.userId_line.text()
            user_role=self.userRole_line.text()
            salt=self.saltMessage_line.text()
            secret_message=self.secretMessage_text.toPlainText()

            self.statusbar_status.showMessage("Creating Files")
            current_timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
            folder_name=f"{user_id}_{user_role}_{current_timestamp}"

            # create this in current directory 
            output_location=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_data", folder_name)
            os.makedirs(output_location) if not os.path.exists(output_location) else None 
            salt_file_name="salt_hexadecimal.data"
            secret_message_file_name="secret_message.pem"

            # write the salt file 
            with open(os.path.join(output_location, salt_file_name), "w") as fp:
                fp.write(salt)

            # write secret message file 
            with open(os.path.join(output_location, secret_message_file_name), "w") as fp:
                fp.write(secret_message)

            self.show_write_successful_message(output_location)                

            # show the successful key files created message 
            self.statusbar_status.showMessage("Complete")

        except Exception as e:
            print (e)


    def get_token_data(self):

        # get the details 
        try:
            self.statusbar_status.showMessage("Validating")
            admin_password=self.validate_string_data(self.adminPassword_line.text(), "Admin Password")
            user_id=self.validate_string_data(self.userId_line.text(), "User ID") 
            user_role=self.validate_string_data(self.userRole_line.text(), "User Role")
            database_location=self.connectionString_text.toPlainText()

            # Connect to Admin Database and get the required information
            self.statusbar_status.showMessage("Querying")

            user_details=self.get_user_details_from_database(admin_password, user_id, user_role, database_location)

            # initalize the model 
            self.initialize_tableview_model() 

            column_names=user_details.get_field_names()
            row_values=user_details.get_field_values()

            # update the model 
            self.update_tableview_model(column_names, row_values)

            # update the status message 
            self.statusbar_status.showMessage("Complete")

        except Exception as e:
            print(e)


    def generate_token_data(self):
        # get the details 
        try:
            self.statusbar_status.showMessage("Validating")
            admin_password=self.validate_string_data(self.adminPassword_line.text(), "Admin Password")
            user_id=self.validate_string_data(self.userId_line.text(), "User ID") 
            user_role=self.validate_string_data(self.userRole_line.text(), "User Role")
            start_date=self.validate_date_data(self.startDate_date.date(), "Start Date")
            end_date=self.validate_date_data(self.endDate_date.date(), "End Date")
            user_passphrase=self.validate_string_data(self.userPassphrase_line.text(), "User Passphrase")
            database_location=self.connectionString_text.toPlainText()

            # Validate start and end date 
            self.validate_start_end_date(start_date, end_date)

            # create input detail object 
            input_details=AdminRecord(user_id=user_id, role=user_role, start_date=start_date, end_date=end_date, passphrase=user_passphrase.encode())

            # get existing details from the database
            valid_record=False
            user_details=self.get_user_details_from_database(admin_password, user_id, user_role, database_location)
            if user_details.user_id:
                valid_record=self.validate_dates_within_range(user_details)

            # if not a valid record then generate the token 
            if not valid_record:
                auth_object=AuthToken()
                key, salt=auth_object.generate_fernet_key_from_passphrase(input_details.passphrase)
                message=self.generate_secret_message(input_details)
                secret_message=auth_object.encrypt_secret_message(key, message)
                input_details.salt=salt
                input_details.secret_message=secret_message
                input_details.private_key=key
                self.insert_user_details(input_details, admin_password)
                user_details=input_details             

            # update GUI with these information 
            self.reset_gui_data()
            self.populate_gui(user_details)

            # initalize the model 
            self.initialize_tableview_model() 

            column_names=user_details.get_field_names()
            row_values=user_details.get_field_values()

            # update the model 
            self.update_tableview_model(column_names, row_values)            

            # update the status message
            self.statusbar_status.showMessage("Complete")

        except Exception as e:
            print(e)


    def get_user_details_from_database(self, admin_password, user_id, user_role, database_location) -> AdminRecord:

        admin_database=AdminDatabase(admin_password, database_location=database_location)
        user_details=admin_database.get_user_details(user_id, user_role)

        if user_details:
            user_details.set_start_date_dtype() 
            user_details.set_end_date_dtype()   

        return user_details


    def initialize_tableview_model(self):
        self.tableView_result_model.removeRows(0, self.tableView_result_model.rowCount())
        self.tableView_result_model.removeColumns(0, self.tableView_result_model.columnCount())


    def update_tableview_model(self, column_names, row_values):
        self.tableView_result_model.setHorizontalHeaderLabels(column_names)
        for idx, row_data in enumerate(row_values):
            item=QStandardItem(row_data)
            self.tableView_result_model.setItem(0, idx, item)

        self.tableView_result_table.setModel(self.tableView_result_model)
        self.tableView_result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    def validate_string_data(self, string_value:str, string_label:str) -> str:
        if not string_value:
            message=f"{string_label} cannot be blank"
            QMessageBox.critical(
                self, "Error", message
            )
            raise ValidationException(message)
        
        return string_value.strip()
    

    def validate_date_data(self, date_variable:QDate, date_label:str) -> datetime.date:
        if not date_variable:
            message=f"{date_label} cannot be blank"
            QMessageBox.critical(
                self, "Error", message
            )
            raise ValidationException(message)
        
        print(date_variable, type(date_variable), type(date_variable.toPyDate()))
        return date_variable.toPyDate()
    

    def validate_start_end_date(self, start_date:datetime.date, end_date:datetime.date) -> None:
        if start_date > end_date:
            message=f"Start Date cannot be after End Date"
            QMessageBox.critical(
                self, "Error", message
            )
            raise ValidationException(message)
        
    def show_write_successful_message(self, output_location):
        message=f"Files are written to {output_location}"
        QMessageBox.information(
            self, "Information", message
        )        


    def validate_dates_within_range(self, user_details:AdminRecord) -> bool:

        current_date=date.today()
        if user_details.start_date >= current_date: 
            if user_details.end_date <= current_date:
                return True 
        return False 


    def generate_secret_message(self, admin_record:AdminRecord):
        message=f"{admin_record.user_id} {admin_record.role} {admin_record.get_start_date_str()} {admin_record.get_end_date_str()}"
        return message


    def insert_user_details(self, input_details:AdminRecord, admin_password:str) -> None:
        """ transfer data from input to user details for """
        admin_database=AdminDatabase(admin_password)
        admin_database.insert_records(input_details)


if __name__=="__main__":
    app=QApplication(sys.argv)
    key_generator=KeyGenerator()
    app.exec()