

APPLICATION_NAME="GunnSutra"
SETUP_CONFIGURATION="setup_configuration.yaml"

SALT_FILE_NAME="salt_hexadecimal.data"
SECRET_FILE_NAME="secret_message.pem"

QSS_1K_FILE="gui_HD.qss"
QSS_2K_FILE="gui_FHD.qss"
QSS_3K_FILE="gui_QHD.qss"
QSS_4K_FILE="gui_UHD.qss"


MESSAGE_LOOKUP={
    "ERRMSG001": "No Authorization Files Found.", 
    "ERRMSG002": "Authorization Data Not Found.", 
    "ERRMSG003": "Authorization Data Not Found.",
    "ERRMSG004": "Invalid datatype conversion requested.",
    "ERRMSG005": "Invalid datatype conversion requested.",
    "ERRMSG006": "Invalid datatype conversion requested.",
    "ERRMSG007": "Invalid user id for associated key.",
    "ERRMSG008": "License key date range in future.",
    "ERRMSG009": "License key date range in past.",
    "ERRMSG010": "Unknown Exception while processing Authorization Request.",
    "ERRMSG011": "User ID not provided.", 
    "ERRMSG012": "Passphrase not provided.",
    "ERRMSG013": "Unable to encrypt secret message. Please investigate.",
    "ERRMSG014": "Unable to decrypt secret message. Please investigate.",
    "ERRMSG015": "Unable to find UI screens",
    "ERRMSG016": "Key not Valid"
}

UI_MODULE_LOOKUP={
    "user_login": "gunnasutra.ui"
}