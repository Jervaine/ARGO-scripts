import os
import threading
import PySimpleGUI as sg
import mechanize
import functions as func
import logging
import glob


# Functions
def run_cif_import():
    logging.info("Running CIF Import")
    br = mechanize.Browser()
    br.add_password("http://localhost:8080/fcs-webservice/jolokia/exec/com.argodata.fraud:name"
                    "=cifImportJmxService,type=CifImportJmxService/runCifImportNow/1", cif_username, cif_password)
    br.open("http://localhost:8080/fcs-webservice/jolokia/exec/com.argodata.fraud:name=cifImportJmxService,type"
            "=CifImportJmxService/runCifImportNow/1")
    logging.info("CIF Import COMPLETED")

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
path_to_ref_folder = ""
path_to_sus_folder = ""
x937_ext = ".x937"
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
            func.delete_file(os.path.join(path_to_etc, file))
            func.move_file(path_to_config_file, path_to_etc)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL4-'].update(visible=True)

    if event == '-FOLDER2-':
        # zipfile =  C:\Users\Kasey\Desktop\test\On_US_DATA_UTD.zip
        zipfile = values['-FOLDER2-']
        print(zipfile)
        # filename = On_US_DATA_UTD
        filename = zipfile.split('/')[-1].split('.')[0]
        print(filename)
        # data_dir = C:\Users\Kasey\Desktop\test\On_US_DATA_UTD
        import_folder_location = OASIS_folder_location + '/' + filename
        print(import_folder_location)
        func.extract_zip(import_folder_location, zipfile)
        print("Extracting Data file")
        name = import_folder_location.split('/')[-1].split('.')[0]
        print(name)
        # Get directory name of the landing zone directory
        landing_path = None
        path_to_aif_folder = None
        for folder_name in os.listdir(import_folder_location):
            if 'landing' in folder_name and os.path.isdir(os.path.join(import_folder_location, folder_name)):
                # landing_path = C:\Users\Kasey\Desktop\test\On_US_DATA\ON_US_import-landing-zones
                landing_path = os.path.join(import_folder_location, folder_name)
            elif 'AIF' in folder_name and os.path.isdir(os.path.join(import_folder_location, folder_name)):
                # path_to_aif_folder = C:\Users\Kasey\Desktop\test\On_US_DATA\AIF files
                path_to_aif_folder = os.path.join(import_folder_location, folder_name)
            # You can continue more elif for each directory you need.

        # path_to_config_file = C:\Users\Kasey\Desktop\test\On_US_DATA\ON_US_import-landing-zones\argoAifConfig.xml
        path_to_config_file = os.path.join(landing_path, 'argoAifConfig.xml')

        # Here you would parse the argoAifConfig.xml file for the file location
        # aif_parse_directory = ???? however you read the xml for '/data/aif-load'


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

        # this is meant to search through all the directories in the data directory based on 'aif' in file name or with .x937 extenstion for those files. Need to get the CIF files first
        # it does not work still and its all still garbage
        pattern = os.path.join(
            os.path.expanduser('~'),
            import_folder_location,
            'aif*'
        )


        allfiles = os.listdir(import_folder_location)
        for f in allfiles:

            if f.endswith('.csv'):

                if matching_file in glob(import_folder_location):
                    with open(matching_file, 'r') as file:
                        func.move_file(path_to_aif_folder + '/' + file, OASIS_folder_location + '/data/aif-load')

            if f.endswith('.done'):
                flag += 1

        for matching_file in glob.glob(import_folder_location):
             with open(matching_file, 'r') as f:
                 func.move_file(path_to_aif_folder + '/' + file, OASIS_folder_location + '/data/aif-load')


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
        # call imports
        for file in os.listdir(path_to_aif_folder):
            func.move_file(path_to_aif_folder + '/' + file, OASIS_folder_location + '/data/aif-load')
        for file in os.listdir(path_to_ref_folder):
            func.move_file(path_to_ref_folder + '/' + file, OASIS_folder_location + '/data/cash-letter-import')
        for file in os.listdir(path_to_sus_folder):
            func.move_file(path_to_sus_folder + '/' + file, OASIS_folder_location + '/data/cash-letter-import')

        # check for .done, and empty import folders to show completion
        read_cif_folder(OASIS_folder_location + "/data/cif-load")

        window[f'-COL5-'].update(visible=False)
        window[f'-COL6-'].update(visible=True)

    if event == '-I THREAD DONE-':
        break

window.close()
quit()
