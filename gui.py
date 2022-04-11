import PySimpleGUI as sg
import zipfile
import shutil
import os
import subprocess
import pyautogui
import time
import threading
from ctypes import *


# Functions
def extract_install_package(directory, install_zip):
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)


def move_customer_package(directory, customer_zip):
    shutil.move(customer_zip, (directory + "/customer/argo-customer-fraud-argo-4.2.7.0-package (5).zip"))


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
    time.sleep(5)
    pyautogui.press('enter')
    ok = windll.user32.BlockInput(False)
    window.write_event_value("-CI THREAD DONE-", "DONE")


def run_installer(host_name_, db_username_, db_password_, logical_db_name_, windows_username_, windows_password_,
                  directory, event_obj):
    directory += "/bin/installer.bat"
    p = subprocess.Popen(['runas', '/profile', '/user:' + windows_username_,
                          directory],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    ok = windll.user32.BlockInput(True)
    time.sleep(5)
    pyautogui.typewrite(windows_password_)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.typewrite("1")
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite("1")
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite(host_name_)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite(db_username_)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite(db_password_)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite(logical_db_name_)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    ok = windll.user32.BlockInput(False)
    window.write_event_value("-WARNING-", "warning")
    flag = event_obj.wait()
    if flag:
        pyautogui.typewrite('y')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.typewrite('delete')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.typewrite('I')
        pyautogui.press('enter')




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

layout = [[sg.Column(welcome_page, key='-COL1-'), sg.Column(folder_select_page, visible=False, key='-COL2-'),
           sg.Column(get_credentials_page, visible=False, key='-COL3-'),
           sg.Column(run_customer_installer_page, visible=False, key='-COL4-'),
           sg.Column(get_info_installer, visible=False, key='-COL5-'),
           sg.Column(run_installer_page, visible=False, key='-COL6-'),
           sg.Column(warning_page, visible=False, key='-COL7-')]]

# Start GUI
window = sg.Window('Oasis Build Installer', layout, resizable=True)
# Behavior of GUI
folder_location = ""
path_to_install_zip_file = ""
path_to_customer_zip_file = ""
customer_folder_location = ""
windows_username = ""
windows_password = ""
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
            extract_install_package(folder_location, path_to_install_zip_file)
            move_customer_package(folder_location, path_to_customer_zip_file)
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=True)
    if event == '-FOLDER-':
        folder_location = values['-FOLDER-']
        path_to_install_zip_file = folder_location + "/argo-fraud-4.2.7.0-install-package (4).zip"
        path_to_customer_zip_file = folder_location + "/argo-customer-fraud-argo-4.2.7.0-package (5).zip"
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



window.close()
