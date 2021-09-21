from database_manager import Database
from encrypter import encrypt, decrypt, password
from const import *
from Crypto.Hash import SHA256
import time


class PWManager:
    def __init__(self, currentDB):
        self.db = db = Database(currentDB)

    def valudate_password(self, password):
        try:
            enc_key = SHA256.new((password).encode('utf-8')).digest().hex() 
            result = decrypt(key=enc_key.encode(), source=SECRET_KEY)
            if result == RESULT:
                set_password(enc_key)
                return True
            return False
        except ValueError as e:
            return False
        
    def add_password(self):
        app_name = input("Enter the App/Site name: ")
        url = input("Enter the url (if exist): ")
        username = input("Enter username used: ")
        user_email = input("Enter email used(if used):")
        while True:
            want_pass= input("Do you want me to generate a password for you? (y/n) :")
            if want_pass == "y":
                plaintext = input("Ok, Just enter a plain text (eg. I like Pancakes): ")
                length = input("Enter the length of password[default : 16]: ")
                
                
                user_password = password(plaintext=plaintext, app_name=app_name, length=int(length) if length.isnumeric() else 16)
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


    def find_info(self):
        result = self.db.find_info()
        if type(result.desc).__name__ == "list":
            try:
                myTable = PrettyTable(["  User Name","  Email","  URL","  App Name"])
                for data in result.desc:
                    myTable.add_row(data[1:])
                    
                print(myTable)
            except Exception:
                print(f"""+{"  User Name" : <30}+{"  Email" : <30}+{'  URL' : <30}+{'  App Name' : <30}+""", end="")
                for data in result.desc:
                    print(f"\n|{'-'*30}|{'-'*30}|{'-'*30}|{'-'*30}|\n|{data[2]: <30}|{data[1]: <30}|{data[3]: <30}|{data[4]: <30}|", end="")
            
        else:
            print("No data present.")
        print()

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

    def delete_data(self):
        value = input("Enter the app name you want to delete: ")
        result = self.db.delete_data_with(field="app_name", value=value)
        if result.type == "RESULT":
            print(result.desc)
        else:
            print(result)


if __name__=="__main__":
    pas = SHA256.new((input("Enter a password: ")).encode('utf-8')).digest().hex()
    print("Copy an past the following text in const.py in the varible SECRET_KEY",encrypt(key=pas, source=RESULT))
    
    


