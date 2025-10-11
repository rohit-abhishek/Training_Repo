import base64 
import os 
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AuthToken:
    """ mathods to authenticate user entered passphrase and salt message """

    def encrypt_secret_message(self, key:bytes, secret_message:str):
        crypto_object=Fernet(key)
        secret_message_encoded=crypto_object.encrypt(secret_message.encode())
        return secret_message_encoded
    
    def decrypt_secret_message(self, key:bytes, secret_message_encoded:str):
        crypto_object=Fernet(key)
        secret_message=crypto_object.decrypt(secret_message_encoded.encode())
        return secret_message


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
    

    def get_key_from_passphrase_and_salt(self, user_passphrase, salt) -> bytes:
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