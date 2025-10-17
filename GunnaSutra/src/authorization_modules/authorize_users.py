import base64 
import os
import sys 
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from exception_modules import ApplicationInterrput, CustomException
from datetime import datetime 
from utility_modules.contants import MESSAGE_LOOKUP, SALT_FILE_NAME, SECRET_FILE_NAME
from utility_modules import FileLocator

class AuthToken:
    """ mathods to authenticate user entered passphrase and salt message """

    def __init__(self, user_id:str, passphrase:str):

        self.user_id=user_id 
        self.passphrase=passphrase


    def validate_auth_token(self):
        """ Validate Auth token by performing series of operations """

        # get the salt and secrement message files 
        salt_file_locator=FileLocator(SALT_FILE_NAME)
        secret_file_locator=FileLocator(SECRET_FILE_NAME)

        # get file location 
        self.__salt_file_location=salt_file_locator.get_system_location()
        self.__secret_file_location=secret_file_locator.get_system_location()

        # read the salt file 
        self.__get_salt_file_data() 

        # read the secret message file 
        self.__get_secret_file_data()

        # convert salt and secret message string type to bytes 
        self.__salt_data=self.hexstring_to_bytes(self.__salt_data)
        self.__secret_message=self.string_to_bytes(self.__secret_message)

        # convert passphrase from string to bytes 
        self.passphrase=self.string_to_bytes(self.passphrase)

        # get key from passphrase and salt message
        self.get_key_from_passphrase_and_salt()

        # get decoded message using generated key 
        secret_message_decoded=self.decrypt_secret_message()

        # validate secret message
        return self.validate_secret_message(secret_message_decoded)


    def __get_salt_file_data(self):
        try:
            with open(self.__salt_file_location, "r") as fp:
                self.__salt_data=fp.readlines()[0]
        except: 
            message_key="ERRMSG001"
            self.raise_custom_error(message_key)

        if not self.__salt_data:
            message_key="ERRMSG002"
            self.raise_custom_error(message_key)            


    def __get_secret_file_data(self):
        try:
            with open(self.__secret_file_location, "r") as fp:
                self.__secret_message=fp.readlines()[0]
        except: 
            message_key="ERRMSG001"
            self.raise_custom_error(message_key)        

        if not self.__secret_message:
            message_key="ERRMSG003"
            self.raise_custom_error(message_key)            

   
    def string_to_bytes(self, data:str) -> bytes:
        if isinstance(data, str):
            return data.encode()
        elif isinstance(data, bytes):
            return data 
        else:
            message_key="ERRMSG004"
            raise ApplicationInterrput(message_key, MESSAGE_LOOKUP.get(message_key, ""))
        
        
    def bytes_to_string(self, data_bytes:bytes) -> str:
        if isinstance(data_bytes, bytes):
            return data_bytes.decode()
        elif isinstance(data_bytes, str):
            return data_bytes 
        else:
            message_key="ERRMSG005"
            raise ApplicationInterrput(message_key, MESSAGE_LOOKUP.get(message_key, ""))
        

    def hexstring_to_bytes(self, data:str) -> bytes:
        if isinstance(data, str):
            return bytes.fromhex(data)
        message_key="ERRMSG006"
        raise ApplicationInterrput(message_key, MESSAGE_LOOKUP.get(message_key, ""))
        
        
    def encrypt_secret_message(self) -> bytes:
        try: 
            crypto_object=Fernet(self.__key)
            secret_message_encoded=crypto_object.encrypt(self.__secret_message)
            return secret_message_encoded
        except Exception as e:
            message_key="ERRMSG013"
            raise CustomException(message_key, MESSAGE_LOOKUP.get(message_key, ""))
    

    def decrypt_secret_message(self) -> bytes:
        try:
            crypto_object=Fernet(self.__key)
            secret_message=crypto_object.decrypt(self.__secret_message)
            return secret_message
        except Exception as e:
            message_key='ERRMSG014'
            raise CustomException(message_key, MESSAGE_LOOKUP.get(message_key, ""))


    def generate_fernet_key_from_passphrase(self) -> tuple[bytes, bytes]:
        self.__salt_data=os.urandom(16)
        kdf=PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32, 
            salt=self.__salt_data,
            iterations=1200000
        )
        self.__key=base64.urlsafe_b64encode(kdf.derive(self.passphrase))
    

    def get_key_from_passphrase_and_salt(self) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.__salt_data,
            iterations=1200000,
        )
        self.__key=base64.urlsafe_b64encode(kdf.derive(self.passphrase))


    def validate_secret_message(self, secret_message_bytes:bytes) -> bool:
        secret_message=self.bytes_to_string(secret_message_bytes)

        return_flag=False 

        user_id, role, start_date_string, end_date_string=secret_message.split(" ")

        # validate user id 
        if user_id.strip() != self.user_id.strip():
            message_key="ERRMSG007"
            raise ApplicationInterrput(message_key, MESSAGE_LOOKUP.get(message_key, ""))
            
        # no validation for role 
        # get current date 
        current_date=datetime.now().date()
        start_date=datetime.strptime(start_date_string, "%Y-%m-%d").date()
        end_date=datetime.strptime(end_date_string, "%Y-%m-%d").date()
        
        if current_date < start_date and current_date < end_date:
            message_key="ERRMSG008"
            raise ApplicationInterrput(message_key, MESSAGE_LOOKUP.get(message_key, ""))

        if current_date > start_date and current_date > end_date:
            message_key="ERRMSG009"
            raise ApplicationInterrput(message_key, MESSAGE_LOOKUP.get(message_key, ""))

        if current_date >= start_date and current_date <= end_date and user_id.strip()==self.user_id.strip():
            return_flag=True 

        return return_flag
    
    
    def raise_custom_error(self, message_key):
        message_text=MESSAGE_LOOKUP.get(message_key)
        raise CustomException(message_key, message_text)    