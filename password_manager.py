from database_manager import Database
from encrypter import encrypt, decrypt, password
from example_psql import *
from Crypto.Hash import SHA256
#from main import type
import time
import functools

#db = Database(CURRENTDB_TYPE)

class PWManager:
    def __init__(self, currentDB):
        self.db = db = Database(currentDB)

    def valudate_password(self, password):
        try:
            enc_key = SHA256.new((password).encode('utf-8')).digest().hex() 
            result = decrypt(key=enc_key.encode(), source=SECRET_KEY)
            if result == "Hello Vignesh.":
                set_password(enc_key)
                return True
            return False
        except ValueError as e:
            return False
    '''
    def make_secure(access_level, func2, func):
        def decorator(func, func2):
            @functools.wraps(func)
            def secure_func(*args, **kwargs):
                if access_level == "High":
                    return func(*args, **kwargs)
                else:
                    return func2()
                    

            return secure_func(func2)
        return decorator(func=func,func2=func2)

    def increse_level():
        if input("Do you want to increse access level : ")=="y":
            set_user_level("High")'''

    #@make_secure(get_user_level(), func=add_password, func2=increse_level)
    def add_password(self):
        app_name = input("Enter the App/Site name: ")
        url = input("Enter the url (if exist): ")
        username = input("Enter username used: ")
        user_email = input("Enter email used(if used):")
        while True:
            want_pass= input("Do you want me to generate a password for you? (y/n) :")
            if want_pass == "y":
                plaintext = input("Ok, Just enter a plain text (eg. I like Pancakes): ")
                length = int(input("Enter the length of password[default : 16]: "))
                user_password = password(plaintext=plaintext, app_name=app_name, length=length)
                print("Your Password is : ", user_password)
                break
            elif want_pass == "n":
                user_password = input("Enter the password: ")
                break
        user_password = encrypt(key=get_password(), source=user_password)
        result = self.db.store_passwords(password=user_password, user_email=user_email, username=username, url=url, app_name=app_name)
        if result.type == "RESULT":
            print(result.desc)
        else:
            print(result)


    def password_of(self, app_name):
        result = self.db.find_password(app_name)
        real_pass= result.desc
        if result.type == "RESULT":
            try:
                if real_pass != "No data found.":
                    real_pass = decrypt(key=get_password().encode() ,source=real_pass)
                print(real_pass)
            except ValueError as e:
                if DEBUG == True:
                    print("Decrypter cannot decrypt ", real_pass)
                print(f"Got error '{e}' which is not excepted. (May be the data stored with external sources which i don't suppot)")
        
    
    def change_password(self):
        app_name = input("Enter the App/site name which you want to chanre password: ")
        password = input("Enter the new password: ")
        conformation = input("Are you sure you want to change password(y/n): ")
        if conformation == "y":
            encrypted = encrypt(key=get_password(), source=password)
            result = self.db.change_password_to(encrypted, app_name)
            if result.type == "RESULT":
                print(result.desc)
            else:
                print(result)
        else:
            print("Password did not changed..")

    #@make_secure(get_user_level())
    def delete_data():
        value = input("Enter the app name you want to delete: ")
        result = self.db.delete_data_with(field="app_name", value="value")
        if result.type == "RESULT":
            print(result.desc)
        else:
            print(result)

    

#pw = PWManager(CURRENTDB_TYPE)
#pw.add_password()
#pw.delete_data()

if __name__=="__main__":
    st = "HI i am vignesh"
    print(split(st, " "))
    

def password_of(app_name):
    encrypted_pass = find_password(app_name)
    #print(encrypted_pass)
    real_pass=encrypted_pass
    if encrypted_pass[0:6] != "[ERROR]":
        try:
            real_pass = decrypt(key=get_password().encode() ,source=encrypted_pass)
        except ValueError as e:
            print("this -->",e)
    return real_pass
 
def change_password():
    app_name = input("Enter the App/site name which you want to chanre password: ")
    password = input("Enter the new password: ")
    conformation = input("Are you sure you want to change password(y/n): ")
    if conformation == "y":
        encrypted = encrypt(key=get_password(), source=password)
        change_password_to(encrypted, app_name)
    else:
        print("Password did not changed..")
    

def add_password():
    app_name = input("Enter the App/Site name: ")
    url = input("Enter the url (if exist): ")
    username = input("Enter username used: ")
    user_email = input("Enter email used(if used):")
    while True:
        want_pass= input("Do you want me to generate a password for you? (y/n) :")
        if want_pass == "y":
            plaintext = input("Ok, Just enter a plain text (eg. I like Pancakes): ")
            length = int(input("Enter the length of password[default : 16]: "))
            user_password = password(plaintext=plaintext, app_name=app_name, length=length)
            print("Your Password is : ", user_password)
            break
        elif want_pass == "n":
            user_password = input("Enter the password: ")
            break
    user_password = encrypt(key=get_password(), source=user_password)
    print(store_passwords(password=user_password, user_email=user_email, username=username, url=url, app_name=app_name))

