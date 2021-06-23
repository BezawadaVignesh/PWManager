from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyfiglet import figlet_format
from termcolor import cprint
from rich import print

from password_manager import PWManager
#from example_psql import SECRET_KEY

import time
import getpass
import os

def print_icon():
    cprint(figlet_format('_ Vignesh _ Manager 1 0'),'yellow', attrs=['bold'])
    

def print_info():
    print("""
    1. Add a password.
    2. Find a existing password of a site.
    3. Change a existing password of a site.   
    4. Quit.
    """)

def shell():
    print("You are in shell now. Press \q to quit shell.")
    while True:
        request = input("> ")
        if request == "\q":
            print("Closeing shell..\n")
            break
        else:
            request.split(",")

def menu(pm,db="SQLite"):
    print_info()
    
    while(True):
        request = input("> ")
        if request == "1":
            pm.add_password()
        elif request == "2":
            app_name = input("Enter the App/site name: ")
            pm.password_of(app_name)
            
        elif request == "3":
            pm.change_password()

        elif request == "4":
            print("Closing Vigneshmanager1.0 \nScreen will be cleared...")
            input("\nPress any key to countinue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        elif request == "cls" or request == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_icon()
        elif request.lower() == "shell":
            shell()
        else:
            print("I don't know that!")



if __name__ == "__main__":
    pm = PWManager("SQLite")
    os.system('cls' if os.name == 'nt' else 'clear')
    print_icon()
    print()
    print("[bold]VigneshManager1.0 [/bold] allows you to store passwords safely. ")
    print()
    password = getpass.getpass("Please provide the master password of VigneshMaanager1.0:")
    
    if pm.valudate_password(password):
        print("[green]You are in ...[/green]")
        menu(pm)
    else:
        print("[red]No luck :([/red]")
    



def loginInChrome(url, username, password):
    driver = webdriver.Chrome(r"chromedriver.exe")

    driver.get(url) # "http://www.github.com/login"

    #my_username ="vigneshbezawada3@gmail.com"
    #my_password= "B1921117589v"

    username_input_box = driver.find_element_by_name("login")
    password_input_box = driver.find_element_by_name("password")
    sign_up_button = driver.find_element_by_name("commit")

    username_input_box.clear()
    username_input_box.send_keys(username)
    time.sleep(1)
    password_input_box.clear()
    password_input_box.send_keys(password)

    time.sleep(1)
    sign_up_button.click()

    time.sleep(30)
    driver.close()