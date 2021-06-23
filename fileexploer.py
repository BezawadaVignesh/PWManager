# Python program to create
# a file explorer in Tkinter
'''
# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog

# Function for opening the
# file explorer window
def browseFiles():
	filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))
	
	# Change label contents
	label_file_explorer.configure(text="File Opened: "+filename)
	
	
																								
# Create the root window
window = Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("500x500")

#Set window background color
window.config(background = "white")

# Create a File Explorer label
label_file_explorer = Label(window,
							text = "File Explorer using Tkinter",
							width = 100, height = 4,
							fg = "blue")

	
button_explore = Button(window,
						text = "Browse Files",
						command = browseFiles)

button_exit = Button(window,
					text = "Exit",
					command = exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

button_explore.grid(column = 1, row = 2)

button_exit.grid(column = 1,row = 3)

# Let the window wait for any events
window.mainloop()
'''
import base64
import os
import time
import sys

pw = "password"   #Dedault Password
encode = base64.b64encode(pw.encode())

def goto(linenum):
    global line
    line = linenum

line = 1
while True:
    pw = str(input("Enter your password for Lock or Unlock your folder: "))
    print(base64.b64decode(encode))

    if pw == base64.b64decode(encode).decode():
    # Change Dir Path where you have Locker Folder
        os.chdir("C:\Users\Lokanadh\Documents\vignesh\python\crome")
    # If Locker folder or Recycle bin does not exist then we will be create Locker Folder 
        if not os.path.exists("Locker"):
            if not os.path.exists("Locker.{645ff040-5081-101b-9f08-00aa002f954e}"):
                os.mkdir("Locker")
            else:
                os.popen('attrib -h Locker.{645ff040-5081-101b-9f08-00aa002f954e}')
                os.rename("Locker.{645ff040-5081-101b-9f08-00aa002f954e}","Locker")
                sys.exit()
        else:
            os.rename("Locker","Locker.{645ff040-5081-101b-9f08-00aa002f954e}")
            os.popen('attrib +h Locker.{645ff040-5081-101b-9f08-00aa002f954e}')
            sys.exit()
        
    else:
        print("Wrong password!, Please Enter right password")
        time.sleep(5)
        goto(1)
