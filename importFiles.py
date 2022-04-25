import zipfile
import shutil
import os
import threading
from datetime import date
import time
from typing import Iterator
import PySimpleGUI as sg
import win32service
import win32serviceutil  # pip install pywin32
import mechanize  # pip install mechanize


# Functions

# non-blocking tail
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


def extract_file_package(directory, install_zip):
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)


def move_files(directory, files):
    allfiles = os.listdir(files)
    for f in allfiles:
        shutil.move(files + "\\" + f, directory + "\\" + f)


def replace_file(directory, files):
    file = 'argoAifConfig.xml'
    path = os.path.join(directory, file)
    os.remove(path)
    shutil.move(files, directory)


def restart_services():
    service_name = "ArgoFraudComplianceService"
    if win32serviceutil.QueryServiceStatus(service_name)[1] == win32service.SERVICE_RUNNING:
        print("Stopping ArgoFraudComplianceService")
        win32serviceutil.StopService(service_name)
    print("ArgoFraudComplianceService Stopped")
    while win32serviceutil.QueryServiceStatus(service_name)[1] == win32service.SERVICE_RUNNING:
        time.sleep(1)
    time.sleep(2)
    if os.path.isdir(OASIS_folder_location + '/logs/fcs-webservice'):
        print("Removing Old Log Files")
        shutil.rmtree(OASIS_folder_location + '/logs/fcs-webservice')
    print("Starting ArgoFraudComplianceService")
    win32serviceutil.StartService(service_name)


def run_cif_import():
    print("Run CIF Import")
    br = mechanize.Browser()
    br.add_password("http://localhost:8080/fcs-webservice/jolokia/exec/com.argodata.fraud:name"
                    "=cifImportJmxService,type=CifImportJmxService/runCifImportNow/1", cif_username, cif_password)
    response = br.open(
        "http://localhost:8080/fcs-webservice/jolokia/exec/com.argodata.fraud:name=cifImportJmxService,type"
        "=CifImportJmxService/runCifImportNow/1")
    print(response)


def read_cif_folder(files):
    allfiles = os.listdir(files)
    amount = len(allfiles)
    amount -= 1
    flag = 0
    for f in allfiles:
        if f.endswith('.done'):
            flag += 1
    if amount != flag:
        print("ERROR with CIF import")


# Layout Pages
sg.theme("SystemDefaultForReal")
welcome_page = [[sg.Text('Oasis Import Files', font=('Arial', 18), size=(40, 2))],
                [sg.Text('Press continue to start the Oasis file import process', size=(40, 3))],
                [sg.Button('Continue', key="wp_continue")]]

OASIS_folder_select_page = [[sg.Text('Select Folder', font=('Arial', 18), size=(40, 2))],
                            [sg.Text('Select the folder containing OASIS build', size=(40, 3))],
                            [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER1-'),
                             sg.FolderBrowse()],
                            [sg.Text('', size=(18, 1))],
                            [sg.Button('Continue', key="OASIS_continue")]]

folder_select_page = [[sg.Text('Select Folder', font=('Arial', 18), size=(40, 2))],
                      [sg.Text('Select the folder containing zip file', size=(40, 3))],
                      [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER2-'), sg.FolderBrowse()],
                      [sg.Text('', size=(18, 1))],
                      [sg.Button('Continue', key="fs_continue")]]

get_credentials_page = [[sg.Text('CIF import Credentials', font=('Arial', 18), size=(40, 2))],
                        [sg.Text('Enter credentials to be able to execute CIF import', size=(40, 4))],
                        [sg.Text('Username ', size=(18, 1)), sg.InputText()],
                        [sg.Text('Password ', size=(18, 1)), sg.InputText(password_char="*")],
                        [sg.Text('', size=(18, 1))],
                        [sg.Button('Continue', key="gc_continue")]]

run_restart_OASIS_page = [[sg.Text('Restarting OASIS', font=('Arial', 18), size=(40, 2))],
                          [sg.Text('Press continue to restart OASIS', size=(40, 3))],
                          [sg.Button('Continue', key="sr_continue")]]

run_files_page = [[sg.Text('Import files', font=('Arial', 18), size=(40, 2))],
                  [sg.Text('Press continue to run the import files script', size=(40, 3))],
                  [sg.Button('Continue', key="rif_continue")]]

end_files_page = [[sg.Text('Import files complete', font=('Arial', 18), size=(40, 2))],
                  [sg.Text('File import completed, click End to complete process', size=(40, 3))],
                  [sg.Button('End', key="rif_continue")]]

layout = [[sg.Column(welcome_page, key='-COL1-'), sg.Column(OASIS_folder_select_page, visible=False, key='-COL2-'),
           sg.Column(folder_select_page, visible=False, key='-COL3-'),
           sg.Column(get_credentials_page, visible=False, key='-COL4-'),
           sg.Column(run_restart_OASIS_page, visible=False, key='-COL5-'),
           sg.Column(run_files_page, visible=False, key='-COL6-')]]

# Start GUI
window = sg.Window('Oasis Import Files', layout, resizable=True, )
# Behavior of GUI
OASIS_folder_location = ""
path_to_logs = ""
path_to_etc = ""
import_folder_location = ""
path_to_config_file = ""
path_to_aif_folder = ""
path_to_cif_folder = ""
path_to_ref_folder = ""
path_to_sus_folder = ""
cif_username = ""
cif_password = ""
event_obj = threading.Event()
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == 'wp_continue':
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)

    if event == 'OASIS_continue':
        if OASIS_folder_location == "":
            sg.Print('No folder selected')
        else:
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=True)

    if event == '-FOLDER1-':
        OASIS_folder_location = values['-FOLDER1-']
        path_to_logs = OASIS_folder_location + "/logs/fcs-webservice"
        path_to_etc = OASIS_folder_location + "/etc/import-landing-zones"

    if event == 'fs_continue':
        if import_folder_location == "":
            sg.Print('No folder selected')
        else:
            print("Extracting Data file")
            extract_file_package(import_folder_location, import_folder_location + "/On_US_DATA_UTD.zip")
            replace_file(path_to_etc, path_to_config_file)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL4-'].update(visible=True)

    if event == '-FOLDER2-':
        import_folder_location = values['-FOLDER2-']
        path_to_config_file = import_folder_location + "/On_US_DATA/ON_US_import-landing-zones/argoAifConfig.xml"
        path_to_aif_folder = import_folder_location + "/On_US_DATA/AIF files"
        path_to_cif_folder = import_folder_location + "/On_US_DATA/CIF/Richard CIF file"
        path_to_ref_folder = import_folder_location + "/On_US_DATA/Richard Ref and Suspect Image/Reference Images"
        path_to_sus_folder = import_folder_location + "/On_US_DATA/Richard Ref and Suspect Image/Suspect Image"

    if event == 'gc_continue':
        cif_username = values[0]
        cif_password = values[1]
        values.clear()
        window[f'-COL4-'].update(visible=False)
        window[f'-COL5-'].update(visible=True)

    if event == 'sr_continue':
        restart_services()
        # read_fcs_file(OASIS_folder_location)
        move_files(OASIS_folder_location + "/data/cif-load", path_to_cif_folder)
        # Wait until log files are generated
        print("Waiting for log files to be generated")
        while True:
            if os.path.isdir(OASIS_folder_location + '/logs/fcs-webservice'):
                print("Log file generated")
                break
            time.sleep(2)
        # Load log file
        log = None
        for file in os.listdir(OASIS_folder_location + '/logs/fcs-webservice'):
            if 'webservice-' in file:
                log = OASIS_folder_location + '/logs/fcs-webservice/' + file
        # Search Log file for "SYSTEM READY"
        print("Waiting for SYSTEM READY")
        with open(log, 'r') as file:
            x = 0
            for line in follow(file):
                if 'SYSTEM READY' in line:
                    print("SYSTEM READY")
                    break

        run_cif_import()
        window[f'-COL5-'].update(visible=False)
        window[f'-COL6-'].update(visible=True)

    if event == 'rif_continue':
        # call imports
        move_files(OASIS_folder_location + "/data/aif-load", path_to_aif_folder)
        move_files(OASIS_folder_location + "/data/cash-letter-import", path_to_ref_folder)
        move_files(OASIS_folder_location + "/data/cash-letter-import", path_to_sus_folder)

        # check for .done, and empty import folders to show completion
        read_cif_folder(OASIS_folder_location + "/data/cif-load")

        window[f'-COL5-'].update(visible=False)
        window[f'-COL6-'].update(visible=True)

    if event == 'import_done':
        break

window.close()
quit()
