import zipfile
import shutil
import os
import subprocess
import pyautogui
import time

# Extract install package
path_to_install_zip_file = "C:\\Users\\ewanf\\Desktop\\Test\\argo-fraud-4.2.7.0-install-package (4).zip"
directory_to_extract_to = "C:\\Users\\ewanf\\Desktop\\Test"
with zipfile.ZipFile(path_to_install_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)

# Move customer package
path_to_customer_zip_file = "C:\\Users\\ewanf\\Desktop\\Test\\argo-customer-fraud-argo-4.2.7.0-package (5).zip"
directory_to_move_to = "C:\\Users\\ewanf\\Desktop\\Test\\customer\\argo-customer-fraud-argo-4.2.7.0-package (5).zip"
shutil.move(path_to_customer_zip_file, directory_to_move_to)

# Run customer installer
p = subprocess.Popen(['C:/Users/ewanf/Desktop/Test/bin/customerInstaller.bat'],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)
time.sleep(10)
pyautogui.typewrite("I")
pyautogui.press('enter')
time.sleep(10)
pyautogui.press('enter')

# Run installer.bat
p = subprocess.Popen(['C:/Users/ewanf/Desktop/Test/bin/installer.bat'],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(10)
pyautogui.typewrite("1")
pyautogui.press('enter')
time.sleep(2)
pyautogui.typewrite("1")
pyautogui.press('enter')
time.sleep(2)
pyautogui.typewrite("localhost")
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.typewrite("sa")
pyautogui.press('enter')
time.sleep(2)
pyautogui.typewrite("piano1996")
pyautogui.press('enter')
time.sleep(2)
pyautogui.typewrite("master")
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
