import pyrebase
import os

config = {
  "apiKey": "WebApiKey",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": "",
  "serviceAccount": "AdminSDK.json"
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

# Zieldateipfad
datadir = 'DestinationPath'

# Alle Inhalte des Ordners "trips" der Storage-Instanz ausgeben
all_files = storage.child("trips").list_files()

for file in all_files:
    # URL der Datei bestimmen
    # storage.child(file.name).get_url(None)
    url = storage.child(file.name).get_url(None)
    url = str(url)
    # Dateiname in Stücke teilen
    name = file.name.split('/')
    del name[-1]
    name_dir = ''
    # Dateipfad bestimmen
    for part in name:
        name_dir = name_dir + part + '/'   
    # Zielordner auf Existenz prüfen, falls nicht vorhanden, Ordner erstellen
    if not os.path.exists(datadir + name_dir):
        os.makedirs(datadir + name_dir)
    # Falls Datei noch nicht vorhanden, herunterladen
    if not os.path.isfile(datadir + file.name):
        try:
            print("Trying to download File")
            storage.child(file.name).download(datadir + file.name)
        except:
            print("File not existing")
    else:
        print("File already Downloaded")