import os, sys 
import sqlcipher3
from datetime import datetime, date
from dataclasses import dataclass, astuple, fields
from datetime import datetime, date
from threading import local


def get_system_location(file_name:str, folder_location:str=None) -> str:
    """ scan system path for required file name """

    return_location=None 

    # If folder location present 
    if folder_location:
        if os.path.exists(os.path.join(folder_location, file_name)):
            return_location=os.path.join(folder_location, file_name)
            return return_location
        
        for root, dirs, files in os.walk(folder_location):
            if file_name in files: 
                return_location=os.path.join(root, file_name)
                return return_location 

    # If folder location not present
    elif os.path.exists(os.path.join(os.path.dirname(sys.executable), file_name)):
        return_location=os.path.join(os.path.dirname(sys.executable), file_name) 
        return return_location
        
    elif os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)):
        return_location=os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        return return_location
        
    else:
        root=os.path.dirname(os.path.abspath(__file__))
        root_path=get_level_up_location(root, level=2)
        # root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        for root, dirs, files in os.walk(root_path):
            if file_name in files: 
                return_location=os.path.join(root, file_name)
                return return_location 

        # still not found then scan through sys.executable location 
        root=sys.executable
        root_path=get_level_up_location(root, level=2)
        # root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.executable))))
        for root, dirs, files in os.walk(root_path):
            if file_name in files: 
                return_location=os.path.join(root, file_name)
                return return_location
    
    return return_location 


def get_level_up_location(location, level=2):
    new_location=location
    for i in range(0, level):
        new_location=os.path.dirname(new_location)

    return new_location


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
            self.start_date=datetime.strptime(self.start_date[:10], "%Y-%m-%d").date()
    
    def set_end_date_dtype(self):
        if isinstance(self.end_date, str):
            self.end_date=datetime.strptime(self.end_date[:10], "%Y-%m-%d").date()

    def get_start_date_str(self):
        if isinstance(self.start_date, date):
            return datetime.strftime(self.start_date, "%Y-%m-%d")
        return self.start_date
        
    def get_end_date_str(self):
        if isinstance(self.end_date, date):
            return datetime.strftime(self.end_date, "%Y-%m-%d")
        return self.end_date
    
    def get_byte_to_string_format(self, field_name:bytes):
        if isinstance(field_name, bytes):
            return field_name.decode()
        return field_name 
    
    def get_string_to_bytes_format(self, field_name:str):
        if isinstance(field_name, str):
            return field_name.encode()
        return field_name

    def get_field_names(self):
        return ["user_id", "passphrase", "start_date", "end_date"]
    
    def get_field_values(self):
        return [self.user_id, self.role, self.get_start_date_str(), self.get_end_date_str()]


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
    def __init__(self, admin_password, admin_database_name="key_generator_admin.db", admin_table_name="admin_table", database_location=None):

        # assign instance variables 
        self.__admin_password=admin_password
        self.local=local()
        self.__admin_table=admin_table_name
        self.__admin_sql_builder=AdminSqlBuilder(admin_table=self.__admin_table, admin_password=self.__admin_password)

        # get the location of admin database - if not found exit 
        if not database_location:
            self.database_location=get_system_location(admin_database_name)
        else: 
            self.database_location=database_location

        # if still database location not provided or not found then create one the current directory
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