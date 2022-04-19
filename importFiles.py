import zipfile
import shutil
import os
import webbrowser
import threading
import time
import PySimpleGUI as sg
import win32serviceutil


# Functions
def extract_file_package(directory, install_zip):
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)


def move_files(directory, files_zip):
    shutil.move(files_zip, (directory + ""))


# Layout Pages
sg.theme("SystemDefaultForReal")
welcome_page = [[sg.Text('Oasis Import Files', font=('Arial', 18), size=(40, 2))],
                [sg.Text('Press continue to start the Oasis file import process', size=(40, 3))],
                [sg.Button('Continue', key="wp_continue")]]

folder_select_page = [[sg.Text('Select Folder', font=('Arial', 18), size=(40, 2))],
                      [sg.Text('Select the folder containing zip file', size=(40, 3))],
                      [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
                      [sg.Text('', size=(18, 1))],
                      [sg.Button('Continue', key="fs_continue")]]

run_customer_installer_page = [[sg.Text('Run Customer Installer', font=('Arial', 18), size=(40, 2))],
                               [sg.Text('Press continue to run the customer installer script', size=(40, 3))],
                               [sg.Button('Continue', key="rci_continue")]]

layout = [[sg.Column(welcome_page, key='-COL1-'), sg.Column(folder_select_page, visible=False, key='-COL2-'),
           sg.Column(run_customer_installer_page, visible=False, key='-COL3-')]]

# Start GUI
window = sg.Window('Oasis Import Files', layout, resizable=True, )
# Behavior of GUI
folder_location = ""
path_to_install_zip_file = ""
path_to_customer_zip_file = ""
customer_folder_location = ""
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
            extract_file_package(folder_location, path_to_install_zip_file)
            move_files(folder_location, path_to_customer_zip_file)
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
    if event == '-I THREAD DONE-':
        break

window.close()

# Extract data files package
path_to_data_zip_file = "C:\\Users\\Nebula\\Desktop\\On_US_DATA_UTD.zip"
directory_to_extract_to = "C:\\Users\\Nebula\\Desktop"
with zipfile.ZipFile(path_to_data_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)

# Get file path for updated xml file and move it to replace existing one
file = 'argoAifConfig.xml'
path_to_xml_file = "C:\\Users\\Nebula\\Desktop\\On_US_DATA\\ON_US_import-landing-zones\\argoAifConfig" \
                   ".xml "
directory_to_move_to = "C:\\Users\\Nebula\\Desktop\\CLEAN_OASIS\\etc\\import-landing-zones\\examples"
path = os.path.join(directory_to_move_to, file)
os.remove(path)
shutil.move(path_to_xml_file, directory_to_move_to)

# Restart ARGO Fraud Services
serviceName = "ArgoFraudComplianceService"
# win32serviceutil.StartService(serviceName)
# win32serviceutil.RestartService("ArgoFraudComplianceService")

# Run CIF import
webbrowser.open_new('http://localhost:8084/fcs-webservice/jolokia/exec/com.argodata.fraud:name=cifImportJmxService,'
                    'type=CifImportJmxService/runCifImportNow/1')

# Get file paths to each import location and move files
path_to_cif_import_files = "C:\\Users\\Nebula\\Desktop\\On_US_DATA\\CIF\\Richard CIF file"
cif_directory_to_move_to = "C:\\Users\\Nebula\\Desktop\\CLEAN_OASIS\\data\\cif-load"

allfiles = os.listdir(path_to_cif_import_files)
for f in allfiles:
    shutil.move(path_to_cif_import_files + "\\" + f, cif_directory_to_move_to + "\\" + f)

path_to_aif_import_files = "C:\\Users\\Nebula\\Desktop\\On_US_DATA\\AIF files"
aif_directory_to_move_to = "C:\\Users\\Nebula\\Desktop\\CLEAN_OASIS\\data\\aif-load"

allfiles = os.listdir(path_to_aif_import_files)
for f in allfiles:
    shutil.move(path_to_aif_import_files + "\\" + f, aif_directory_to_move_to + "\\" + f)

path_to_cash_letter_import_files_1 = "C:\\Users\\Nebula\\Desktop\\On_US_DATA\\Richard Ref and Suspect " \
                                     "Image\\Reference Images"
path_to_cash_letter_import_files_2 = "C:\\Users\\Nebula\\Desktop\\On_US_DATA\\Richard Ref and Suspect " \
                                     "Image\\Suspect Image"
cash_letter_directory_to_move_to = "C:\\Users\\Nebula\\Desktop\\CLEAN_OASIS\\data\\cash-letter-import"

allfiles = os.listdir(path_to_cash_letter_import_files_1)
for f in allfiles:
    shutil.move(path_to_cash_letter_import_files_1 + "\\" + f, cash_letter_directory_to_move_to + "\\" + f)

allfiles = os.listdir(path_to_cash_letter_import_files_2)
for f in allfiles:
    shutil.move(path_to_cash_letter_import_files_2 + "\\" + f, cash_letter_directory_to_move_to + "\\" + f)


