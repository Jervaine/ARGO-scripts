import PySimpleGUI as sg
import zipfile
import shutil
import os
import subprocess
import pyautogui
import time


# Functions
def extract_install_package(directory, install_zip):
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)


def move_customer_package(directory, customer_zip):
    shutil.move(customer_zip, (directory + "/customer/argo-customer-fraud-argo-4.2.7.0-package (5).zip"))


def run_customer_installer(windows_username_, windows_password_):
    p = subprocess.Popen(['runas', '/profile', '/user:' + windows_username_,
                          'C:/Users/ewanf/Desktop/Test/bin/customerInstaller.bat'],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(5)
    pyautogui.typewrite(windows_password_)
    pyautogui.press('enter')
    pyautogui.typewrite("I")
    pyautogui.press('enter')
    time.sleep(10)
    pyautogui.press('enter')


# Layout Pages
welcome_page = [[sg.Text('Oasis Build Installation', font=('Arial', 18), size=(40, 3))],
                [sg.Text('Press continue to start the Oasis build installation process', size=(40, 5))],
                [sg.Button('Continue', key="wp_continue")]]

folder_select_page = [[sg.Text('Select Folder', font=('Arial', 18), size=(40, 3))],
                      [sg.Text('Select the folder containing zip files', size=(40, 3))],
                      [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
                      [sg.Text('', size=(18, 1))],
                      [sg.Button('Continue', key="fs_continue")]]

get_credentials_page = [[sg.Text('Windows Credentials', font=('Arial', 18), size=(40, 2))],
                        [sg.Text('Enter credentials to be able to run scripts as administrator', size=(40, 4))],
                        [sg.Text('Windows username ', size=(18, 1)), sg.InputText()],
                        [sg.Text('Windows password ', size=(18, 1)), sg.InputText()],
                        [sg.Text('', size=(18, 1))],
                        [sg.Button('Continue', key="gc_continue")]]

run_customer_installer_page = [[sg.Text('Run Customer Installer', font=('Arial', 18), size=(40, 3))],
                               [sg.Text('Press continue to run the customer installer script', size=(40, 5))],
                               [sg.Button('Continue', key="rci_continue")]]

get_info_installer = [[sg.Text('Installer Info', font=('Arial', 18), size=(40, 3))],
                      [sg.Text('Enter information to be able to run the installer script', size=(40, 5))],
                      [sg.Text('Hostname ', size=(18, 1)), sg.InputText()],
                      [sg.Text('Database Username ', size=(18, 1)), sg.InputText()],
                      [sg.Text('Database Password ', size=(18, 1)), sg.InputText()],
                      [sg.Text('Logical DB Name ', size=(18, 1)), sg.InputText()],
                      [sg.Button('Continue', key="gii_continue")]]

layout = [[sg.Column(welcome_page, key='-COL1-'), sg.Column(folder_select_page, visible=False, key='-COL2-'),
           sg.Column(get_credentials_page, visible=False, key='-COL3-'),
           sg.Column(run_customer_installer_page, visible=False, key='-COL4-'),
           sg.Column(get_info_installer, visible=False, key='-COL5-')]]

# Start GUI
window = sg.Window('Oasis Build Installer', layout, resizable=True)
# Behavior of GUI
folder_location = ""
path_to_install_zip_file = ""
path_to_customer_zip_file = ""
customer_folder_location = ""
windows_username = ""
windows_password = ""
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
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=True)
    if event == '-FOLDER-':
        folder_location = values['-FOLDER-']
        path_to_install_zip_file = folder_location + "/argo-fraud-4.2.7.0-install-package (4).zip"
        path_to_customer_zip_file = folder_location + "/argo-customer-fraud-argo-4.2.7.0-package (5).zip"
        extract_install_package(folder_location, path_to_install_zip_file)
        move_customer_package(folder_location, path_to_customer_zip_file)
    if event == 'gc_continue':
        windows_username = values[0]
        windows_password = values[1]
        window[f'-COL3-'].update(visible=False)
        window[f'-COL4-'].update(visible=True)
    if event == 'rci_continue':
        run_customer_installer(windows_username, windows_password)
        window[f'-COL4-'].update(visible=False)
        window[f'-COL5-'].update(visible=True)
    if event == 'gii_continue':


window.close()
