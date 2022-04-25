from typing import Iterator
import time
import zipfile
import shutil
import win32service
import win32serviceutil
import logging
import os

#Generic Functions

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
    with zipfile.ZipFile(install_zip, 'r') as zip_ref:
        zip_ref.extractall(directory)

def delete_file(file):
    name = file.split('/')[-1]
    os.remove(file)
    logging.info(name + " REMOVED")

def move_file(file, destination):
    name = file.split('/')[-1]
    logging.info("MOVING " + name + " to " + destination)
    shutil.move(file, destination)

def stop_service(name):
    if win32serviceutil.QueryServiceStatus(name)[1] == win32service.SERVICE_RUNNING:
        logging.info("STOPPING " + name)
        win32serviceutil.StopService(name)
    else:
        logging.info(name + " already STOPPED")
        return
    while win32serviceutil.QueryServiceStatus(name)[1] == win32service.SERVICE_RUNNING:
        time.sleep(1)
    logging.info(name + " STOPPED")

def delete_dir(directory):
    path = directory.split('/')
    logging.info("Deleting " + path[-1])
    if(os.path.isdir(directory)):
        shutil.rmtree(directory)
        logging.info(path[-1] + " DELETED")
        return
    logging.info(path[-1] + " does NOT exist")

def start_service(name):
    logging.info("STARTING " + name)
    win32serviceutil.StartService(name)
    while win32serviceutil.QueryServiceStatus(name)[1] != win32service.SERVICE_RUNNING:
        time.sleep(1)
    logging.info(name + " STARTED")

def load_log(directory, name):
    for file in os.listdir(directory):
        if name in file:
            log = os.path.joing(directory, file)
            logging.info(file + " LOADED")
            return log