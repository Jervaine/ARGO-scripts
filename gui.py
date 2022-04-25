import PySimpleGUI as sg
import subprocess
import pyautogui
import time
import threading
from ctypes import *
import os
import functions as func

import functions

# Functions
def run_customer_installer(windows_username_, windows_password_, directory):
    directory += "/bin/customerInstaller.bat"
    print(directory)
    p = subprocess.Popen(['runas', '/profile', '/user:' + windows_username_,
                          directory],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)

    ok = windll.user32.BlockInput(True)
    time.sleep(5)
    pyautogui.typewrite(windows_password_)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite("I")
    pyautogui.press('enter')
    time.sleep(7)
    pyautogui.press('enter')
    ok = windll.user32.BlockInput(False)
    window.write_event_value("-CI THREAD DONE-", "DONE")


def run_installer(host_name_, db_username_, db_password_, logical_db_name_, windows_username_, windows_password_,
                  directory, event_obj):
    #Key Phrases
    strings = [
        "What kind of installation is this",
        "Select the type for database",
        "Enter hostname or IP address",
        "How do you want to connect",
        "Enter the port for database",
        "How do you want to authenticate",
        "Enter the username for database",
        "Enter the password for database",
        "Enter the logical database name",
        "Would you like to customize the JDBC URL",
        "Would you like to test these connection settings",
        "Do you want to use encrypted database credentials",
        "Enter the HTTP port for Tomcat",
        "Enter the shutdown port for Tomcat",
        "Enter the port for JMX",
        "Do you want to require a password to connect to JMX",
        "Do you want the installer to try and enable RCSI",
        "Do you want to DROP and RECREATE all of the AML",
        "Are you certain that you want to DROP and RECREATE",
        "Do you want to enable the HOST Web Service",
        "Do you want to enable the OFAC Search Web Service",
        "Do you want to install this as a Windows service",
        "Ready to (I)nstall the above changes",
        "INSTALLATION COMPLETED"
    ]
    #Delete any existing log files for the installer.
    if os.path.isdir(directory + '/logs/installer'):
        for file in os.listdir(directory + '/logs/installer'):
            func.delete_file(os.path.join(directory + '/logs/installer', file))

    #Run Installer Script
    p = subprocess.Popen(['runas', '/profile', '/user:' + windows_username_,
                          directory + '/bin/installer.bat'],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    ok = windll.user32.BlockInput(True)
    time.sleep(5)
    pyautogui.typewrite(windows_password_)
    pyautogui.press('enter')
    time.sleep(5)

    #Get path of log file
    log = None
    for file in os.listdir(directory + '/logs/installer'):
        if 'installer-' in file:
            log = directory + '/logs/installer/' + file

    # Tail the log file and run all against string[x]
    with open(log, 'r') as file:
        x = 0
        for line in func.follow(file):
            if strings[x] in line:
                time.sleep(.2)
                if x == 0 or x == 1 or x == 3 or x == 5:
                    pyautogui.typewrite("1")
                    pyautogui.press('enter')
                elif x == 2:
                    pyautogui.typewrite(host_name_)
                    pyautogui.press('enter')
                elif x == 6:
                    pyautogui.typewrite(db_username_)
                    pyautogui.press('enter')
                elif x == 7:
                    pyautogui.typewrite(db_password_)
                    pyautogui.press('enter')
                elif x == 8:
                    pyautogui.typewrite(logical_db_name_)
                    pyautogui.press('enter')
                elif x == 17:
                    ok = windll.user32.BlockInput(False)
                    window.write_event_value("-WARNING-", "warning")
                    flag = event_obj.wait()
                    if flag:
                        ok = windll.user32.BlockInput(True)
                        pyautogui.typewrite("y")
                        pyautogui.press('enter')
                    else:
                        x += 30
                elif x == 18:
                    pyautogui.typewrite("delete")
                    pyautogui.press('enter')
                elif x == 22:
                    pyautogui.typewrite("I")
                    pyautogui.press('enter')
                elif x == 23:
                    pyautogui.press('enter')
                    time.sleep(1)
                    pyautogui.press('enter')
                    break
                else:
                    pyautogui.press('enter')
                x += 1
                if x > 30:
                    quit()
    window.write_event_value("-B THREAD DONE-", "Done")
    ok = windll.user32.BlockInput(False)


def run_system_config(directory, windows_username_):
    strings = [
        "Select configuration process",             #2
        "Have you stopped the Argo Fraud service",  #y
        "Have you backed up your database",         #y
        "Ready to (I)nstall the above changes",     #I
        "INSTALLATION COMPLETED SUCCESSFULLY"       #enter
    ]

    directory += "./bin/configure.bat"
    p = subprocess.Popen(['runas', '/profile', '/user:' + windows_username_,
                          directory],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    ok = windll.user32.BlockInput(True)
    time.sleep(5)
    pyautogui.typewrite('2')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('y')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('y')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('i')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('a')
    pyautogui.press('enter')
    ok = windll.user32.BlockInput(False)
    window.write_event_value("-S THREAD DONE-", "DONE")


def run_bank_config(directory, windows_username_):
    strings = [
        "Select configuration process",             #1
        "Have you stopped the Argo Fraud service",  #y
        "Have you backed up your database",         #y
        "What is the bank name",                    #bank
        "Ready to (I)nstall the above changes",     #I
        "INSTALLATION COMPLETED SUCCESSFULLY"       #enter
    ]
    directory += "./bin/configure.bat"
    p = subprocess.Popen(['runas', '/profile', '/user:' + windows_username_,
                          directory],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    ok = windll.user32.BlockInput(True)
    time.sleep(5)
    pyautogui.typewrite('1')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('y')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('y')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('argo')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('I')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('a')
    pyautogui.press('enter')
    ok = windll.user32.BlockInput(False)
    window.write_event_value("-CI THREAD DONE-", "DONE")


# Layout Pages
welcome_page = [[sg.Text('Oasis Build Installation', font=('Arial', 18), size=(40, 2))],
                [sg.Text('Press continue to start the Oasis build installation process', size=(40, 3))],
                [sg.Button('Continue', key="wp_continue")]]

folder_select_page = [[sg.Text('Select Folder', font=('Arial', 18), size=(40, 2))],
                      [sg.Text('Select the folder containing zip files', size=(40, 3))],
                      [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
                      [sg.Text('', size=(18, 1))],
                      [sg.Button('Continue', key="fs_continue")]]

get_credentials_page = [[sg.Text('Windows Credentials', font=('Arial', 18), size=(40, 2))],
                        [sg.Text('Enter credentials to be able to run scripts as administrator', size=(40, 4))],
                        [sg.Text('Windows username ', size=(18, 1)), sg.InputText()],
                        [sg.Text('Windows password ', size=(18, 1)), sg.InputText(password_char="*")],
                        [sg.Text('', size=(18, 1))],
                        [sg.Button('Continue', key="gc_continue")]]

run_customer_installer_page = [[sg.Text('Run Customer Installer', font=('Arial', 18), size=(40, 2))],
                               [sg.Text('Press continue to run the customer installer script', size=(40, 3))],
                               [sg.Button('Continue', key="rci_continue")]]

get_info_installer = [[sg.Text('Installer Info', font=('Arial', 18), size=(40, 2))],
                      [sg.Text('Enter information to be able to run the installer script', size=(40, 4))],
                      [sg.Text('Hostname ', size=(18, 1)), sg.InputText()],
                      [sg.Text('Database Username ', size=(18, 1)), sg.InputText()],
                      [sg.Text('Database Password ', size=(18, 1)), sg.InputText(password_char="*")],
                      [sg.Text('Logical DB Name ', size=(18, 1)), sg.InputText()],
                      [sg.Text('', size=(18, 1))],
                      [sg.Button('Continue', key="gii_continue")]]

run_installer_page = [[sg.Text('Run Installer', font=('Arial', 18), size=(40, 2))],
                      [sg.Text('Press continue to run the installer script', size=(40, 3))],
                      [sg.Button('Continue', key="ri_continue")]]

warning_page = [[sg.Text('Warning!', font=('Arial', 18), size=(40, 2))],
                [sg.Text('Are you sure you want to drop and recreate database?', size=(40, 3))],
                [sg.Button('Yes', key="wap_yes")],
                [sg.Button('No', key="wap_no")]]

run_bank_config_page = [[sg.Text('Run Installer', font=('Arial', 18), size=(40, 2))],
                   [sg.Text('Press continue to run the bank installer script', size=(40, 3))],
                   [sg.Button('Continue', key="bank_continue")]]

run_system_config_page = [[sg.Text('Run Installer', font=('Arial', 18), size=(40, 2))],
                     [sg.Text('Press continue to run the system installer script', size=(40, 3))],
                     [sg.Button('Continue', key="sys_continue")]]

layout = [[sg.Column(welcome_page, key='-COL1-'), sg.Column(folder_select_page, visible=False, key='-COL2-'),
           sg.Column(get_credentials_page, visible=False, key='-COL3-'),
           sg.Column(run_customer_installer_page, visible=False, key='-COL4-'),
           sg.Column(get_info_installer, visible=False, key='-COL5-'),
           sg.Column(run_installer_page, visible=False, key='-COL6-'),
           sg.Column(warning_page, visible=False, key='-COL7-'),
           sg.Column(run_bank_config_page, visible=False, key='-COL8-'),
           sg.Column(run_system_config_page, visible=False, key='-COL9-')]]

# Start GUI
window = sg.Window('Oasis Build Installer', layout, resizable=True)
# Behavior of GUI
folder_location = ""
path_to_install_zip_file = ""
path_to_customer_zip_file = ""
customer_folder_location = ""
windows_username = ""
windows_password = ""
sys_location = ""
bank_location = ""
host_name = ""
db_username = ""
db_password = ""
logical_db_name = ""
event_obj = threading.Event()


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == 'wp_continue':
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)
    if event == 'fs_continue':
        if folder_location == "":
            sg.Print('No folder selected')
        else:
            func.extract_zip(folder_location, path_to_install_zip_file)
            func.move_file(path_to_customer_zip_file, folder_location + "/customer/customer.zip")
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=True)
    if event == '-FOLDER-':
        folder_location = values['-FOLDER-']
        for file in os.listdir(folder_location):
            if 'install' in file:
                path_to_install_zip_file = folder_location + '/' + file
            if 'customer' in file:
                path_to_customer_zip_file = folder_location + '/' + file
    if event == 'gc_continue':
        windows_username = values[0]
        windows_password = values[1]
        values.clear()
        window[f'-COL3-'].update(visible=False)
        window[f'-COL4-'].update(visible=True)
    if event == 'rci_continue':
        threading.Thread(target=run_customer_installer, args=(windows_username, windows_password, folder_location),
                         daemon=True).start()
    if event == '-CI THREAD DONE-':
        window[f'-COL4-'].update(visible=False)
        window[f'-COL5-'].update(visible=True)
    if event == 'gii_continue':
        host_name = values[2]
        db_username = values[3]
        db_password = values[4]
        logical_db_name = values[5]
        window[f'-COL5-'].update(visible=False)
        window[f'-COL6-'].update(visible=True)
    if event == 'ri_continue':
        threading.Thread(target=run_installer, args=(
            host_name, db_username, db_password, logical_db_name, windows_username, windows_password, folder_location,
            event_obj),
                         daemon=True).start()
    if event == '-WARNING-':
        if sg.Window("Warning!", [[sg.Text("Drop and recreate the database?\nThis action is non-reversible!")],
                                  [sg.Yes(), sg.No()]]).read(close=True)[0] == "Yes":
            event_obj.set()
        else:
            break
    if event == '-I THREAD DONE-':
        window[f'COL-6'].update(visible=False)
        window[f'COL-8'].update(visible=True)
    if event == 'sys_continue':
        threading.Thread(target=run_bank_config, args=(
            sys_location, windows_username),
                         daemon=True).start()
    if event == '-S THREAD DONE':
        window[f'COL-8'].update(visible=False)
        window[f'COL-9'].update(visible=True)
    if event == 'bank_continue':
        threading.Thread(target=run_system_config, args=(
            bank_location, windows_username),
                         daemon=True).start()
    if event == '-B THREAD DONE-':
        break

window.close()
quit()
