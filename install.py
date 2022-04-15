import traceback
from tkinter import filedialog as fd
from tkinter import *
import shutil
import subprocess
import pyautogui
import logging

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
window.geometry('300x350')

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

filetypes = (
    ('Zip File', '*.zip'),
    ('All Files', '*.*')
)
#Choose Argo Install Package
print("Select Install Package")
installfile = fd.askopenfilename(
    title='Select Install Package',
    initialdir='/',
    filetypes=filetypes)
print(installfile + "selected")

#Choose Argo Customer Package
print("Select Customer Package")
customerfile = fd.askopenfilename(
    title='Select Customer File',
    initialdir='/',
    filetypes=filetypes)
print(customerfile + "selected")

#Extract Install Package
directory = fd.askdirectory()
shutil.unpack_archive(installfile, directory)

#Install Customer File Package
shutil.move(customerfile, directory + '/customer/customer.zip')
p = subprocess.Popen([directory + '/bin/customerInstaller.bat'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
while True:
    try:
        line = p.stdout.readline()
    except (AttributeError) as e:
        print(e)
        continue
    print(line)
    if "- Ready to (I)nstall the above changes?" in line:
        p.stdin.write("I")
        p.stdin.write('\n')
    if "INSTALLATION COMPLETED SUCCESSFULLY" in line:
        subprocess.Popen.kill(p)

#Run Installer
p = subprocess.Popen([directory + '/bin/installer.bat'], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
while True:
    try:

        line = p.stdout.readline()
    except Exception as e:
        logging.error(traceback.format_exc())
        continue
    print(line)
    if "Add a new bank" in line:
        pyautogui.typewrite("1")
        pyautogui.press('enter')
    elif "Select the type for database" in line:
        pyautogui.typewrite("1")
        pyautogui.press('enter')
    elif "hostname or IP" in line:
        pyautogui.typewrite(host)
        pyautogui.press('enter')
    elif "How do you want to connect" in line:
        pyautogui.typewrite("1")
        pyautogui.press('enter')
    elif "port for database" in line:
        pyautogui.press('enter')
    elif "How do you want to authenticate" in line:
        pyautogui.typewrite("1")
        pyautogui.press('enter')
    elif "username for database" in line:
        pyautogui.typewrite(username)
        pyautogui.press('enter')
    elif "password for database" in line:
        pyautogui.typewrite(password)
        pyautogui.press('enter')
    elif "logical database name" in line:
        pyautogui.typewrite(database)
        pyautogui.press('enter')
    elif "new JDBC URL" in line:
        pyautogui.typewrite("n")
        pyautogui.press('enter')
    elif "test these connection settings" in line:
        pyautogui.typewrite("y")
        pyautogui.press('enter')
    elif "encrypted database credentials" in line:
        pyautogui.typewrite("y")
        pyautogui.press('enter')
    elif "HTTP port" in line:
        pyautogui.press('enter')
    elif "port for JMX" in line:
        pyautogui.press('enter')
    elif "require a password to" in line:
        pyautogui.typewrite("y")
        pyautogui.press('enter')
    elif "DROP and RECREATE all" in line:
        pyautogui.typewrite("y")
        pyautogui.press('enter')
    elif "DROP and RECREATE the" in line:
        pyautogui.typewrite("delete")
        pyautogui.press('enter')
    elif "enable the HOST Web" in line:
        pyautogui.typewrite("n")
        pyautogui.press('enter')
    elif "OFAC Search Web" in line:
        pyautogui.typewrite("n")
        pyautogui.press('enter')
    elif "Install this as a Windows" in line:
        pyautogui.typewrite("n")
        pyautogui.press('enter')
    elif "Ready to (I)nstall the above" in line:
        pyautogui.typewrite("I")

        pyautogui.press('enter')
    elif "INSTALLATION COMPLETED SUCCESSFULLY" in line:
        subprocess.Popen.kill(p)

    quit()
