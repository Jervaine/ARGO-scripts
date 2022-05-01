import os
import threading
import PySimpleGUI as sg
import mechanize
import functions as func
import logging
import re

# Functions
def run_cif_import():
    logging.info("Running CIF Import")
    br = mechanize.Browser()
    br.add_password("http://localhost:8080/fcs-webservice/jolokia/exec/com.argodata.fraud:name"
                    "=cifImportJmxService,type=CifImportJmxService/runCifImportNow/1", cif_username, cif_password)
    br.open("http://localhost:8080/fcs-webservice/jolokia/exec/com.argodata.fraud:name=cifImportJmxService,type"
            "=CifImportJmxService/runCifImportNow/1")
    logging.info("CIF Import COMPLETED")

def read_completion_folder(option, files):
    allfiles = os.listdir(files)
    amount = len(allfiles)
    amount -= 1
    flag = 0

    # For CIF import check
    if option == 1:
        for f in allfiles:
            if f.endswith('.done'):
                flag += 1
        if amount != flag:
            print("ERROR with CIF import. Check logs")

    # For AIF import check
    if option == 2:
        if not amount == flag:
            print("Error with AIF file import. Check logs")

    # For Cash Letter import check
    if option == 3:
        for f in allfiles:
            if f.endswith('.Complete'):
                flag += 1
        if amount != flag:
            print("ERROR with Cash Letter import. Check logs")


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
                      [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER2-'), sg.FileBrowse()],
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

completed_files_page = [[sg.Text('Import files', font=('Arial', 18), size=(40, 2))],
                        [sg.Text('Press continue to run the import files script', size=(40, 3))],
                        [sg.Button('Continue', key="rif_continue")]]

layout = [[sg.Column(welcome_page, key='-COL1-'), sg.Column(OASIS_folder_select_page, visible=False, key='-COL2-'),
           sg.Column(folder_select_page, visible=False, key='-COL3-'),
           sg.Column(get_credentials_page, visible=False, key='-COL4-'),
           sg.Column(run_restart_OASIS_page, visible=False, key='-COL5-'),
           sg.Column(completed_files_page, visible=False, key='-COL6-')]]

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
path_to_cli_folder = ""
path_to_cli_complete = ""
path_to_aif_complete = ""
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
        path_to_cif_folder = OASIS_folder_location + "/data/cif-load"
        path_to_aif_folder = OASIS_folder_location + "/data/aif-load"
        path_to_aif_complete = OASIS_folder_location + "data/import-file-repo/1/argoAif/Complete"
        path_to_cli_folder = OASIS_folder_location + "/data/cash-letter-import"
        path_to_cli_complete = OASIS_folder_location + "/data/repo/cash-letter-import"

    if event == 'fs_continue':
        if import_folder_location == "":
            sg.Print('No folder selected')
        else:

            # ERROR for some reason changing argoAifConfig.xml is not working right????????

            func.delete_file(os.path.join(path_to_etc, 'argoAifConfig.xml'))
            func.move_file(path_to_config_file, path_to_etc)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL4-'].update(visible=True)

    if event == '-FOLDER2-':
        zipfile = values['-FOLDER2-']
        filename = zipfile.split('/')[-1].split('.')[0]
        import_folder_location = os.path.join(OASIS_folder_location, filename).replace("\\","/")

        func.extract_zip(import_folder_location, zipfile)
        print("Extracting Data file")
        # begin search for files and move them
        for root, dirs, files in os.walk(import_folder_location):
            for name in files:

                if re.search("aif", name):
                    print(name)
                    obj = os.path.join(root, name).replace("\\","/")
                    func.move_file(obj, path_to_aif_folder)

                elif re.search(".x937", name):
                    print(name)
                    obj = os.path.join(root, name).replace("\\","/")
                    func.move_file(obj, path_to_cli_folder)

                elif re.search(".csv", name):
                    print(name)
                    obj = os.path.join(root, name).replace("\\","/")
                    func.move_file(obj, path_to_cif_folder)

                elif name == 'argoAifConfig.xml':
                    path_to_config_file = os.path.join(root, name).replace("\\","/")


    if event == 'gc_continue':
        cif_username = values[0]
        cif_password = values[1]
        values.clear()
        window[f'-COL4-'].update(visible=False)
        window[f'-COL5-'].update(visible=True)

    if event == 'sr_continue':
        service = "ArgoFraudComplianceService"
        func.stop_service(service)
        func.delete_dir(OASIS_folder_location + '/logs/fcs-webservice')
        func.start_service(service)

        # Wait until log files are generated
        func.wait_for_dir(OASIS_folder_location + '/logs/fcs-webservice')
        # Load log file
        log = func.load_log(OASIS_folder_location + '/logs/fcs-webservice', 'webservice-')
        # Search Log file for "SYSTEM READY"
        func.argo_ready(log)
        run_cif_import()
        window[f'-COL5-'].update(visible=False)
        window[f'-COL6-'].update(visible=True)

    if event == 'rif_continue':
        # check for .done, and empty import folders to show completion
        read_completion_folder(1, path_to_cif_folder)

        # ERROR this AIF completion check does not work
        # Wait until directory is generated
        # func.wait_for_dir(path_to_aif_complete)
        # read_completion_folder(2, path_to_aif_complete)
        read_completion_folder(3, path_to_cli_complete)

        window[f'-COL5-'].update(visible=False)
        window[f'-COL6-'].update(visible=True)
        sleep(2)
        break

window.close()
quit()
