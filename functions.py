from typing import Iterator
import time
import zipfile
import shutil
import win32service
import win32serviceutil
import os
#import subprocess

#Generic Functions
# def uninstall_service(directory):
#     print("UNINSTALLING Windows Service")
#     p = subprocess.Popen([directory + '/bin/uninstallWindowsService.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
#     p.wait()
#
# def install_service(directory):
#     print("INSTALLING Windows Service")
#     p = subprocess.Popen([directory + '/bin/installWindowsService.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
#     p.wait()

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

def extract_zip(directory, install_zip):
    name = install_zip.split('/')[-1]
    print("EXTRACTING " + name)
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)

def delete_file(file):
    os.remove(file)
    print(file + " REMOVED")

def del_all_files(directory):
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            delete_file(os.path.join(directory, file))

def file_exists(directory, file):
    while True:
        for f in os.listdir(directory):
            if file in f:
                return

def move_file(file, destination):
    name = file.split('/')[-1]
    # print("MOVING " + name + " to " + destination)
    print("MOVING " + file + " to " + destination)
    shutil.move(file, destination)

def stop_service(name):
    if win32serviceutil.QueryServiceStatus(name)[1] == win32service.SERVICE_RUNNING:
        print("STOPPING " + name)
        win32serviceutil.StopService(name)
        win32serviceutil.WaitForServiceStatus(name, win32service.SERVICE_STOPPED, 5)
    else:
        print(name + " already STOPPED")
        return
    print(name + " STOPPED")

def delete_dir(directory):
    path = directory.split('/')
    print("Deleting " + path[-1])
    if(os.path.isdir(directory)):
        shutil.rmtree(directory)
        print(path[-1] + " DELETED")
        return
    print(path[-1] + " does NOT exist")

def start_service(name):
    print("STARTING " + name)
    win32serviceutil.StartService(name)
    win32serviceutil.WaitForServiceStatus(name, win32service.SERVICE_RUNNING, 5)
    print(name + " STARTED")

def load_log(directory, name):
    for file in os.listdir(directory):
        if name in file:
            log = os.path.join(directory, file)
            print(file + " LOADED")
            return log

def wait_for_dir(directory):
    folder = directory.split('/')[-1]
    print("Waiting for " + folder + " to be CREATED")
    while True:
        if os.path.isdir(directory):
            print(folder + " CREATED")
            break
        time.sleep(2)

def argo_ready(log):
    with open(log, 'r') as file:
        for line in follow(file):
            if 'SYSTEM READY' in line:
                print("SYSTEM READY")
                break