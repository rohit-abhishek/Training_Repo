import base64
from dataclasses import dataclass, astuple, fields
import sqlite3
import os, sys
import sqlcipher3
import ttkbootstrap as tkb
import getpass 

from ttkbootstrap.dialogs import Messagebox
from datetime import datetime, date 
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from threading import local
from exception_modules import ProcessingException, ValidationException


def get_system_location(file_name:str) -> str:
    """ scan system path for required file name """

    if os.path.exists(os.path.join(os.path.dirname(sys.executable), file_name)):
        return os.path.join(os.path.dirname(sys.executable), file_name) 
    
    elif os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    
    else:
        root_path=os.path.dirname(os.path.abspath(__file__))
        for root, dirs, files in os.walk(root_path):
            if file_name in files: 
                return os.path.join(root, file_name)
            
        # still not found then scan through sys.executable location 
        root_path=os.path.dirname(sys.executable)
        for root, dirs, files in os.walk(root_path):
            if file_name in files: 
                return os.path.join(root, file_name)
    
    return None 


@dataclass 
class AdminRecord:

    """ user_id: end user 
        role: end user role 
        start_date: end user start date 
        end_date: end user end date 

        secret_message: encrypted message for other application to validate the authorization 
        passphrase: admin provided passphrase 
        salt: salt for cooking 32 byte encrption key

        In other app, user will be prompted to provide passphrase. with passphrase and salt (included in executable) - generate encryption key. 
        Use this key to decode secret_message (included in executable) for authorization 
    """

    user_id:str=None 
    role:str=None 
    start_date:date=None 
    end_date:date=None 

    # for encryption 
    secret_message:bytes=None 
    passphrase:bytes=None 
    salt:bytes=None 
    private_key:bytes=None 

    def set_start_date_dtype(self):
        if isinstance(self.start_date, str):
            self.start_date=datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S").date()
    
    def set_end_date_dtype(self):
        if isinstance(self.end_date, str):
            self.end_date=datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S").date()

    def get_start_date_str(self):
        if isinstance(self.start_date, date):
            return datetime.strftime(self.start_date, "%Y-%m-%d")
        return self.start_date
        
    def get_end_date_str(self):
        if isinstance(self.end_date, date):
            return datetime.strftime(self.end_date, "%Y-%m-%d")
        return self.end_date


class AdminSqlBuilder:

    def __init__(self, admin_table:str, admin_password:str):
        self.__admin_table=admin_table
        self.__admin_password=admin_password

    def get_pragma_key_sql(self) -> str:
        sql_ = f""" PRAGMA key = '{self.__admin_password}' """
        return sql_
    

    def get_admin_table_ddl(self) -> str:
        sql_ = f""" CREATE TABLE IF NOT EXISTS {self.__admin_table} (
                    id                        INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id                   TEXT, 
                    role                      TEXT, 
                    start_date                datetime, 
                    end_date                  datetime,
                    secret_message            BLOB, 
                    passphrase                BLOB, 
                    salt                      BLOB, 
                    private_key               BLOB
        )"""
        return sql_


    def get_admin_insert_sql(self) -> str:
    
        # column_names = tuple([field.name for field in fields(admin_record)])
        sql_ = f""" insert into {self.__admin_table} 
        (user_id, role, start_date, end_date, secret_message, passphrase, salt, private_key) 
        values (?, ?, ?, ?, ?, ?, ?, ?) """
        return sql_


    def get_user_details_sql(self, role:str) -> str:

        sql_=f""" select user_id, role, start_date, end_date, secret_message, passphrase, salt, private_key
                    from {self.__admin_table} where user_id=?
              """
        
        if role and role!="": 
            sql_ = sql_ + f""" and role=? """ 
        
        sql_ = sql_ + f""" order by id desc """ 
        return sql_
    
    def update_user_details_sql(self) -> str:
        
        sql_=f""" update {self.__admin_table} set role=?, 
                                                  start_date=?, 
                                                  end_date=?,
                                                  secret_message=?,
                                                  passphrase=?,
                                                  salt=?, 
                                                  private_key=?
                  where user_id=? """



class AdminDatabase: 
    def __init__(self, admin_password, admin_database_name="key_generator_admin.db", admin_table_name="admin_table"):

        # assign instance variables 
        self.__admin_password=admin_password
        self.local=local()
        self.__admin_table=admin_table_name
        self.__admin_sql_builder=AdminSqlBuilder(admin_table=self.__admin_table, admin_password=self.__admin_password)

        # get the location of admin database - if not found exit 
        self.database_location=get_system_location(admin_database_name)

        # if not found then create one 
        if not self.database_location:
            self.database_location=os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                admin_database_name)
            self.create_database()
            

    def __get_cipher_connection(self) -> sqlcipher3.Connection:

        if not hasattr(self.local, "connection"):
            self.local.connection=sqlcipher3.connect(self.database_location, check_same_thread=False)
        return self.local.connection
    

    def __disconnect(self, conn):

        conn.close()

        if hasattr(self.local, "connection"):
            delattr(self.local, "connection")
        

    def create_database(self) -> None:
        
        # get connection and cursor handles
        conn=self.__get_cipher_connection()
        crsr=conn.cursor()

        # execute sql to set password 
        crsr.execute(self.__admin_sql_builder.get_pragma_key_sql())
        crsr.execute(self.__admin_sql_builder.get_admin_table_ddl())
        conn.commit()

        self.__disconnect(conn)


    def insert_records(self, admin_record:AdminRecord) -> None:

        # get connection and cursor handles
        conn=self.__get_cipher_connection()
        crsr=conn.cursor()

        # execute sql to set password 
        crsr.execute(self.__admin_sql_builder.get_pragma_key_sql())
        crsr.execute(self.__admin_sql_builder.get_admin_insert_sql(), astuple(admin_record))
        conn.commit()

        self.__disconnect(conn)

    
    def get_user_details(self, user_id, role) -> AdminRecord:

        # get connection and cursor handles
        conn=self.__get_cipher_connection()
        crsr=conn.cursor()

        user_record=AdminRecord()

        # execute sql to set password 
        crsr.execute(self.__admin_sql_builder.get_pragma_key_sql())
        crsr.execute(self.__admin_sql_builder.get_user_details_sql(role), (user_id, role))

        # get the result 
        result=crsr.fetchone()
        if result:
            user_record=AdminRecord(*result)

        conn.commit() 
        self.__disconnect(conn)

        return user_record


class KeyGenerator(tkb.Frame):
    def __init__(self, parent):
        tkb.Frame.__init__(self, parent) 
        self.parent=parent 
        self.initialize_gui()


    def initialize_gui(self):
        self.parent.title("Key Generator for Nirnayo Sutra")
        self.pack(side="top", expand=True, fill="both")

        # create widget for admin password at the top 
        self.create_admin_password_entry(row=0, column=0) 

        # add a separator 
        separator=tkb.Separator(self)
        separator.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # create widget for entering user details 
        self.create_end_user_name_entry(row=2, column=0)

        # create widget for entering user role
        self.create_end_user_role_entry(row=3, column=0)

        # create start and end date widgets 
        self.create_start_date_entry(row=4, column=0)
        self.create_end_date_entry(row=5, column=0)

        # create entry for admin to create passphrase for user 
        self.create_end_user_passphrase_entry(row=6, column=0)

        # add separator
        separator=tkb.Separator(self)
        separator.grid(row=7, column=0, columnspan=3, sticky="ew", padx=10, pady=10)       

        # create text box for secret message which should be copied and given to other app 
        self.create_secret_message_textbox(row=8, column=0) 
        self.create_salt_message_textbox(row=9, column=0)

        # add separator 
        separator=tkb.Separator(self)
        separator.grid(row=10, column=0, columnspan=3, sticky="ew", padx=10, pady=10)     

        # add buttons for processing the requests
        self.create_database_retrieve_button(row=11, column=0)
        self.create_generate_token_button(row=11, column=1)
        self.create_clear_form_button(row=11, column=2)


    def create_admin_password_entry(self, row=0, column=0): 
        admin_password_label=tkb.Label(self, text="Admin Password")
        admin_password_label.grid(row=row, column=column, sticky="w", padx=10, pady=10)

        self.admin_password_entry=tkb.Entry(self, show="*")
        self.admin_password_entry.grid(row=row, column=column+1, columnspan=2, sticky="ew", padx=10, pady=10)
        self.admin_password_entry.insert(0, "")


    def create_end_user_name_entry(self, row=0, column=0):
        user=getpass.getuser()

        # set user details  
        user_label = tkb.Label(self, text = f"User ID")
        user_label.grid(row=row, column=column, sticky="w", padx=10, pady=10)

        self.user_entry = tkb.Entry(self)
        self.user_entry.grid(row=row, column=column+1, columnspan=2, sticky="ew", padx=10, pady=10)
        self.user_entry.insert(0, user)


    def create_end_user_role_entry(self, row=0, column=0):
        # set role details 
        role_label = tkb.Label(self, text = f"Role")
        role_label.grid(row=row, column=column, sticky="w", padx=10, pady=10)

        self.role_entry = tkb.Entry(self)
        self.role_entry.grid(row=row, column=column+1, columnspan=2, sticky="ew", padx=10, pady=10)
        self.role_entry.insert(0, "admin")


    def create_start_date_entry(self, row=0, column=0):
        start_date_default = date.today()
        
        # create label for start date 
        start_date_label = tkb.Label(self, text="Start Date")
        start_date_label.grid(row=row, column=column, padx=10, sticky="w", pady=10)

        # set the start date label
        self.start_date_calendar = tkb.DateEntry(self, dateformat="%m/%d/%Y")
        self.start_date_calendar.grid(row=row, column=column+1, columnspan=2, padx=10, sticky="ew", pady=10)
        self.start_date_calendar.set_date(start_date_default)


    def create_end_date_entry(self, row=0, column=0):
        end_date_default = date.today()

        # set the end date label 
        end_date_label = tkb.Label(self, text="End Date")
        end_date_label.grid(row=row, column=column, padx=10, sticky="w", pady=10)

        self.end_date_calendar = tkb.DateEntry(self, dateformat="%m/%d/%Y")
        self.end_date_calendar.grid(row=row, column=column+1, columnspan=2, padx=10, sticky="ew", pady=10)
        self.end_date_calendar.set_date(end_date_default)


    def create_end_user_passphrase_entry(self, row=0, column=0):
        # add passphrase details for admin to code and provide to app user 
        user_passphrase_label=tkb.Label(self, text="User Passphrase")
        user_passphrase_label.grid(row=row, column=column, sticky="w", padx=10, pady=10)

        self.user_passphrase_entry=tkb.Entry(self)
        self.user_passphrase_entry.grid(row=row, column=column+1, sticky="ew", columnspan=2, padx=10, pady=10)


    def create_secret_message_textbox(self, row=0, column=0):
        secret_message_label=tkb.Label(self, text="Secret Message")
        secret_message_label.grid(row=row, column=column, sticky="w", padx=10, pady=10)

        self.secret_message_text=tkb.Text(self, height=5, width=20)
        self.secret_message_text.grid(row=row, column=column+1, columnspan=2, sticky="nsew", padx=10, pady=10)


    def create_salt_message_textbox(self, row=0, column=0):
        salt_message_label=tkb.Label(self, text="Salt (Hexadecimal Format)")
        salt_message_label.grid(row=row, column=column, sticky="w", padx=10, pady=10)

        self.salt_message_text=tkb.Text(self, height=5, width=20)
        self.salt_message_text.grid(row=row, column=column+1, columnspan=2, sticky="nsew", padx=10, pady=10)


    def create_database_retrieve_button(self, row=0, column=0):
        # create retrieve button 
        self.retrieve_data_button=tkb.Button(self, text="Get Token Data", 
                                             command=lambda: self.retreive_token_details(self.user_entry, self.role_entry, self.admin_password_entry))
        self.retrieve_data_button.grid(row=row, column=column, sticky="ew", padx=10, pady=10, ipadx=5)


    def create_generate_token_button(self, row=0, column=0):
        # create button to generate token 
        self.generate_token_button = tkb.Button(self, text="Generate Token", 
                                                command=lambda : self.generate_token(self.start_date_calendar, self.end_date_calendar, self.user_entry, self.role_entry, self.admin_password_entry, self.user_passphrase_entry))
        self.generate_token_button.grid(row=row, column=column, sticky="ew", padx=10, pady=10, ipadx=5)


    def create_clear_form_button(self, row=0, column=0):
        # create retrieve button 
        self.clear_form_button=tkb.Button(self, text="Clear Form", 
                                             command=lambda: self.reset_gui_data())
        self.clear_form_button.grid(row=row, column=column, sticky="ew", padx=10, pady=10, ipadx=5)


    def retreive_token_details(self, user_widget, role_widget, admin_password_widget):
        user_id=user_widget.get()
        role=role_widget.get()
        admin_password=admin_password_widget.get()

        user_id=self.validate_string_variable(user_id, "User Id")
        admin_password=self.validate_string_variable(admin_password, "Admin Password")

        # get user details and update the front end
        user_details=self.get_user_database_details(admin_password, user_id, role)
        if user_details.user_id:
            self.reset_gui_data()
            self.populate_gui(user_details)


    def reset_gui_data(self):
        self.user_entry.delete(0, "end")
        self.role_entry.delete(0, "end")
        # self.user_passphrase_entry.delete(0, "end")
        self.secret_message_text.delete("1.0", "end")
        self.salt_message_text.delete("1.0", "end")


    def populate_gui(self, admin_record:AdminRecord):
        self.user_entry.insert("end", admin_record.user_id)
        self.role_entry.insert("end", admin_record.role)
        self.start_date_calendar.set_date(admin_record.start_date)
        self.end_date_calendar.set_date(admin_record.end_date)
        self.secret_message_text.insert("end", admin_record.secret_message)
        self.salt_message_text.insert("end", admin_record.salt.hex())


    def generate_token(self, start_date_widget, end_date_widget, user_widget, role_widget, admin_password_widget, user_passphrase_widget):
        
        # get the data from the 
        user_id=user_widget.get()
        role=role_widget.get() 
        start_date=start_date_widget.get_date() 
        end_date=end_date_widget.get_date() 
        admin_password=admin_password_widget.get() 
        user_passphrase=user_passphrase_widget.get()

        # validate string and date variables 
        user_id=self.validate_string_variable(user_id, "User Id")
        role=self.validate_string_variable(role, "Role")
        start_date=self.validate_date_variable(start_date, "Start Date")
        end_date=self.validate_date_variable(end_date, "End Date")
        admin_password=self.validate_string_variable(admin_password, "Admin Password")
        user_passphrase=self.validate_string_variable(user_passphrase, "User Passphrase")

        # validate start and end date 
        self.validate_start_end_date(start_date, end_date)

        # get input details in admin_record format 
        input_details=AdminRecord(user_id=user_id, role=role, start_date=start_date, end_date=end_date, passphrase=user_passphrase.encode())

        # get details from the database if exits 
        user_details=self.get_user_database_details(admin_password, user_id, role)

        # validate if record is within the date range
        valid_record=False 
        if user_details.user_id:
            valid_record=self.validate_dates_within_range(user_details)
        
        # if record already exists and valid - return the data else insert the data
        if not valid_record: 
            key, salt=self.generate_fernet_key_from_passphrase(input_details.passphrase)
            print("Please Note Salt Value: ", salt)
            secret_message=self.generate_secret_message(key, input_details)
            input_details.salt=salt 
            input_details.secret_message=secret_message
            input_details.private_key=key
            self.insert_user_details(input_details, admin_password)
            user_details=input_details

        # update GUI with these information 
        self.reset_gui_data()
        self.populate_gui(user_details)


    def generate_fernet_key_from_passphrase(self, user_passphrase:bytes) -> tuple[bytes, bytes]:

        if isinstance(user_passphrase, str):
            user_passphrase=user_passphrase.encode() 

        salt=os.urandom(16)
        kdf=PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32, 
            salt=salt,
            iterations=1200000
        )
        key=base64.urlsafe_b64encode(kdf.derive(user_passphrase))
        return key, salt
    

    def get_key_from_passphrase_and_salt(self, user_passphrase, salt):
        if isinstance(user_passphrase, str):
            user_passphrase=user_passphrase.encode() 
        
        if isinstance(salt, str):
            salt=bytes.fromhex(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1_200_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(user_passphrase))
        return key
        
    
    def generate_secret_message(self, key, admin_record:AdminRecord):
        message=f"""{admin_record.user_id} {admin_record.role} {admin_record.get_start_date_str()} {admin_record.get_end_date_str()}""" 
        crypto_object=Fernet(key)
        secret_message=crypto_object.encrypt(message.encode())
        return secret_message


    def validate_string_variable(self, string_value, string_label) -> str:
        if not string_value:
            message=f"{string_label} cannot be blank"
            Messagebox.show_error(message)
            raise ValidationException(message)
        
        return string_value.strip()

    def validate_date_variable(self, date_variable, date_label) -> date:
        if not date_variable:
            message=f"{date_label} cannot be blank"
            Messagebox.show_error(message)
            raise ValidationException
        
        return date_variable
        
    def validate_start_end_date(self, start_date, end_date) -> None:
        if start_date > end_date:
            message=f"Start Date cannot be after End Date"
            Messagebox.show_error(message)
            raise ValidationException(message)
        
    
    def get_user_database_details(self, admin_password, user_id, role) -> AdminRecord:
        admin_database=AdminDatabase(admin_password)
        # admin_database.create_database()
        user_details=admin_database.get_user_details(user_id, role) 

        # update string datatype to datetime datatype 
        user_details.set_start_date_dtype()
        user_details.set_end_date_dtype()

        return user_details
    
    def validate_dates_within_range(self, user_details:AdminRecord) -> bool:

        current_date=date.today()
        if user_details.start_date >= current_date: 
            if user_details.end_date <= current_date:
                return True 
        return False 
    
    def insert_user_details(self, input_details:AdminRecord, admin_password:str) -> None:
        """ transfer data from input to user details for """
        admin_database=AdminDatabase(admin_password)
        admin_database.insert_records(input_details)


def main():
    try:
        root=tkb.Window()
        key_generator=KeyGenerator(root)
        key_generator.mainloop()
    except Exception as e:
        print(e)


if __name__=="__main__":
    main()
