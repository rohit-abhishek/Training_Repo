import base64 
import os
import sys 
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from exception_modules import ApplicationInterrput, CustomException
from datetime import datetime 
from utility_modules.contants import MESSAGE_LOOKUP

class AuthToken:
    """ mathods to authenticate user entered passphrase and salt message """
   
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
        
        
    def encrypt_secret_message(self, key_bytes:bytes, secret_message_bytes:bytes) -> bytes:
        try: 
            crypto_object=Fernet(key_bytes)
            secret_message_encoded=crypto_object.encrypt(secret_message_bytes)
            return secret_message_encoded
        except Exception as e:
            message_key="ERRMSG013"
            raise CustomException(message_key, MESSAGE_LOOKUP.get(message_key, ""))
    
    def decrypt_secret_message(self, key_bytes:bytes, secret_message_encoded_bytes:bytes) -> bytes:
        try:
            crypto_object=Fernet(key_bytes)
            secret_message=crypto_object.decrypt(secret_message_encoded_bytes)
            return secret_message
        except Exception as e:
            message_key='ERRMSG014'
            raise CustomException(message_key, MESSAGE_LOOKUP.get(message_key, ""))


    def generate_fernet_key_from_passphrase(self, user_passphrase_bytes:bytes) -> tuple[bytes, bytes]:

        salt=os.urandom(16)
        kdf=PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32, 
            salt=salt,
            iterations=1200000
        )
        key=base64.urlsafe_b64encode(kdf.derive(user_passphrase_bytes))
        return key, salt
    

    def get_key_from_passphrase_and_salt(self, user_passphrase_bytes:bytes, salt_bytes:bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=1_200_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(user_passphrase_bytes))
        return key
    

    def validate_secret_message(self, user_id_string:str, secret_message_bytes:bytes) -> bool:
        secret_message=self.bytes_to_string(secret_message_bytes)

        return_flag=False 

        user_id, role, start_date_string, end_date_string=secret_message.split(" ")

        # validate user id 
        if user_id.strip() != user_id_string.strip():
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

        if current_date >= start_date and current_date <= end_date and user_id.strip()==user_id_string.strip():
            return_flag=True 

        return return_flag