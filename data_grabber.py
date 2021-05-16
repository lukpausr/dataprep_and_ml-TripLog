# =============================================================================
# data_grabber
# Download all recorded files (within the app) from Google Firebase and save
# those files in Nextcloud of DHBW-Stuttgart (or any folder, depending on the
# destination folder)
#
# You have to fill in Google API Information. A version with Information
# (should the keys not already be disabled) can be found on the secured
# Nextcloud Instance. Do not push Keys to Github or they will be taken and the
# data will not be secure anymore
#
# Result: Downloads all records from Google Firebase, if not alredy downloaded
# Be careful because of the 1 Gigabyte Download Limit per day
#
# Comment: pyrebase is incompatible with some modules being used for machine
# learning, so two different python environments are required to execute
# everything
# =============================================================================

import pyrebase
import os

###############################################################################
### Pyrebase Config
###############################################################################
config = {
  "apiKey": "WebApiKey",             # Web API Key from firebase
  "authDomain": "",                  # authDomain *.firebaseapp.com
  "databaseURL": "",                 # Can be left empty
  "storageBucket": "",               # Storage bucket adress *.appspot.com
  "serviceAccount": "AdminSDK.json"  # Locally saved Json (AdminSDK) file
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

###############################################################################
### Destination Folder
### Nextcloud Version: 
### *DIRECTORY*:/*FOLDER*/05-Messfahrten_Daten/FirebaseStorageTripData/
###############################################################################
datadir = 'DestinationPath'

# Output all contents of the "trips" folder of the storage instance
all_files = storage.child("trips").list_files()

for file in all_files:
    # Determine URL of the file
    # storage.child(file.name).get_url(None)
    url = storage.child(file.name).get_url(None)
    url = str(url)
    # Split filename into pieces
    name = file.name.split('/')
    del name[-1]
    name_dir = ''
    # Determine file path
    for part in name:
        name_dir = name_dir + part + '/'   
    # Check target folder for existence, if not present, create folder
    if not os.path.exists(datadir + name_dir):
        os.makedirs(datadir + name_dir)
    # If file not yet available, download
    if not os.path.isfile(datadir + file.name):
        try:
            print("Trying to download File")
            storage.child(file.name).download(datadir + file.name)
        except:
            print("File not existing")
    else:
        print("File already Downloaded")