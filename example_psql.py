PGHOST="127.0.0.1"
PGDATABASE="vigneshmanager"
PGUSER="vignesh"
PGPASSWORD=""
PGPORT="5432"
SECRET_KEY="w4Qq3tLgX3vec/aeiXR/ffEXlypDxBpIiqsxoENwlIs="

USER_LEVEL = ""
CURRENTDB_TYPE = "POSTGERSQL"

DATABASE_PATH = "vigneshmanager.db"

DEBUG = False

def set_password(password):
    global PGPASSWORD
    PGPASSWORD = password
    if DEBUG==True:
        print("Password as set to: ", PGPASSWORD)

def set_user_level(level):
    global USER_LEVEL
    USER_LEVEL = level
    if DEBUG == True:
        print(f"User level has been set to : {USER_LEVEL}")

def get_password():
    return PGPASSWORD

def get_user_level():
    return USER_LEVEL
