import traceback
from tkinter import filedialog as fd
from tkinter import *
import shutil
import subprocess
from typing import Iterator

import pyautogui
import logging
import time
import os

username = ""
password = ""
database = ""
host = ""

def dialog():
    global username
    global password
    global database
    global host
    username = usernameEntry.get()
    password = passwordEntry.get()
    database = databaseEntry.get()
    host = hostEntry.get()
    window.destroy()

window = Tk()
window.title('Installation Info')
window.geometry('400x450')

frame = Frame(window)
hostLabel = Label( window, text = 'Hostname or IP: ')
hostLabel.pack(padx=15, pady=5)
hostEntry = Entry(window, bd=5)
hostEntry.pack(padx=15, pady=5)

usernameLabel = Label( window, text = 'Username: ')
usernameLabel.pack(padx=15, pady=5)
usernameEntry = Entry(window, bd=5)
usernameEntry.pack(padx=15, pady=5)

passwordLabel = Label( window, text = 'Password: ')
passwordLabel.pack(padx=15, pady=5)
passwordEntry = Entry(window, show="*", bd=5)
passwordEntry.pack(padx=15, pady=5)

databaseLabel = Label( window, text = 'Logical Database: ')
databaseLabel.pack(padx=15, pady=5)
databaseEntry = Entry(window, bd=5)
databaseEntry.pack(padx=15, pady=5)

okButton = Button(frame, text = "OK", command=dialog)
okButton.pack(side = RIGHT, padx=5)
frame.pack(padx=100, pady=19)

window.mainloop()

# filetypes = (
#     ('Zip File', '*.zip'),
#     ('All Files', '*.*')
# )
# #Choose Argo Install Package
# print("Select Install Package")
# installfile = fd.askopenfilename(
#     title='Select Install Package',
#     initialdir='/',
#     filetypes=filetypes)
# print(installfile + "selected")
#
# #Choose Argo Customer Package
# print("Select Customer Package")
# customerfile = fd.askopenfilename(
#     title='Select Customer File',
#     initialdir='/',
#     filetypes=filetypes)
# print(customerfile + "selected")

#Extract Install Package
directory = fd.askdirectory()
# shutil.unpack_archive(installfile, directory)

#Install Customer File Package
# shutil.move(customerfile, directory + '/customer/customer.zip')
# p = subprocess.Popen([directory + '/bin/customerInstaller.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
#
# time.sleep(5)
# pyautogui.typewrite("I")
# pyautogui.press('enter')
# time.sleep(5)
# pyautogui.press('enter')
#
# subprocess.Popen.kill(p)

#Run Installer

#Strings that the script will search the log file for.
strings = [
    "What kind of installation is this",                    #1          -0
    "Select the type for database",                         #1          -1
    "Enter hostname or IP address",                         #hostname   -2
    "How do you want to connect",                           #1          -3
    "Enter the port for database",                          #default    -4
    "How do you want to authenticate",                      #1          -5
    "Enter the username for database",                      #username   -6
    "Enter the password for database",                      #password   -7
    "Enter the logical database name",                      #database   -8
    "Would you like to customize the JDBC URL",             #default    -9
    "Would you like to test these connection settings",     #default    -10
    "Do you want to use encrypted database credentials",    #default    -11
    "Enter the HTTP port for Tomcat",                       #default    -12
    "Enter the shutdown port for Tomcat",                   #default    -13
    "Enter the port for JMX",                               #default    -14
    "Do you want to require a password to connect to JMX",  #default    -15
    "Do you want instaaler to try and enable RCSI",         #default    -16
    "Do you want to DROP and RECREATE all of the AML",      #y          -17
    "Are you certain that you want to DROP and RECREATE the", #delete   -18
    "Do you want to enable the HOST Web Service",           #default    -19
    "Do you want to enable the OFAC Search Web Service",    #default    -20
    "Do you want to install this as a Windows service",     #default    -21
    "Ready to (I)nstall the above changes",                 #I          -22
    "INSTALLATION COMPLETED SUCCESSFULLY"                   #end        -23
]

#this is a non-blocking tail function.
def follow(file, sleep_sec=.1) -> Iterator[str]:
    line = ''
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        elif sleep_sec:
            time.sleep(sleep_sec)

#delete any existing log files for the installer.
if os.path.isdir(directory + '/logs/installer'):
    for file in os.listdir(directory + '/logs/installer'):
        os.remove(os.path.join(directory + '/logs/installer', file))
#Run the installer.bat script
p = subprocess.Popen([directory + '/bin/installer.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
time.sleep(5)
log = None
#Get path of newly created log file
for file in os.listdir(directory + '/logs/installer'):
    if 'installer-' in file:
        log = directory + '/logs/installer/' + file

#Tail the log file and run all against string[x]
with open(log, 'r') as file:
    x = 0
    for line in follow(file):
        if strings[x] in line:
            time.sleep(.2)
            if x == 0 or x == 1 or x == 3 or x == 5:
                pyautogui.typewrite("1")
                pyautogui.press('enter')
            elif x == 2:
                pyautogui.typewrite(host)
                pyautogui.press('enter')
            elif x == 6:
                pyautogui.typewrite(username)
                pyautogui.press('enter')
            elif x == 7:
                pyautogui.typewrite(password)
                pyautogui.press('enter')
            elif x == 8:
                pyautogui.typewrite(database)
                pyautogui.press('enter')
            elif x == 17:
                pyautogui.typewrite("y")
                pyautogui.press('enter')
            elif x == 18:
                pyautogui.typewrite("delete")
                pyautogui.press('enter')
            elif x == 22:
                pyautogui.typewrite("I")
                pyautogui.press('enter')
            else:
                pyautogui.press('enter')
            x += 1
            print(line)



# p = subprocess.Popen([directory + '/bin/installer.bat'], stdout=subprocess.PIPE, shell=True, universal_newlines=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
#
# for x in range(0, 22, 0):
#     try:
#         line = p.stdout.readline()
#     except Exception as e:
#         logging.error(traceback.format_exc(e))
#         continue
#     print(line)
#
#     if strings[x] in line:
#         if x == 0 or x == 1 or x == 5:
#             pyautogui.typewrite("1")
#             pyautogui.press('enter')
#         elif x == 2:
#             pyautogui.typewrite(host)
#             pyautogui.press('enter')
#         elif x == 6:
#             pyautogui.typewrite(username)
#             pyautogui.press('enter')
#         elif x == 7:
#             pyautogui.typewrite(password)
#             pyautogui.press('enter')
#         elif x == 8:
#             pyautogui.typewrite(database)
#             pyautogui.press('enter')
#         elif x == 9 or x == 17 or x == 18 or x == 19:
#             pyautogui.typewrite("n")
#             pyautogui.press('enter')
#         elif x == 10 or x == 11 or x == 14:
#             pyautogui.typewrite("y")
#             pyautogui.press('enter')
#         elif x == 16:
#             pyautogui.typewrite("delete")
#             pyautogui.press('enter')
#         elif x == 20:
#             pyautogui.typewrite("I")
#             pyautogui.press('enter')
#         else:
#             pyautogui.press('enter')
#         x = x + 1
#
# subprocess.Popen.kill(p)
#
# quit()
