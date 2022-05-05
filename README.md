# ARGO-scripts
### Required Software:
* [Python](https://www.python.org/downloads/)
* Install all required libraries prior to running both scripts using `pip install`
* May need to additionally run `pip install pywin32` in order to Start/Stop "ARGO Fraud Compliance Services" window service

## Project Build
### gui.py
Automates process that creates the OASIS build.
Requires:
* Zip folders of OASIS build and Customer data
* Windows Credentials
* Valid SQL connection

## Import Files
### importFiles.py
Automates process that imports files into the OASIS build.
Requires:
* Zip folder of file data
* JMX command Credentials
* Current running setup of OASIS
