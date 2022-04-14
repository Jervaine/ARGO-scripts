import zipfile
import shutil
import os
import webbrowser
import time
import PySimpleGUI as sg



# Functions
def = extract_file_package(directory, install_zip):
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)

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

# Run CIF import
webbrowser.open_new('http://localhost:8084/fcs-webservice/jolokia/exec/com.argodata.fraud:name=cifImportJmxService,'
                    'type=CifImportJmxService/runCifImportNow/1')
