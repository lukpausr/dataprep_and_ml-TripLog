#  TripLog - Data Analysis and Machine Learning
The following explanation of the scripts is given in german language only.

## Anleitung

### Datenvorverarbeitung
#### Herunterladen der Daten - data_grabber.py
Mit dem Script "data_grabber.py" können die auf der Google Firebase gesammelten Daten gedownloaded werden. 
Ein Script "data_grabber_w_keys.py" findet sich auf der DHBW Nextcloud. Dieses Script sollte nicht weiterverbreitet werden, da es wichtige, persönliche Informationen enthält.
Das Script muss einmalig gestartet werden, es lädt alle neu hinzugekommenen Daten herunter und legt diese in der Nextcloud (bzw. in einem zu definierenden Ordner) ab. Dieser Ordner wird unter folgender Variable definiert.
```python
datadir = '***:/***/05.Messfahrten_Daten/FirebaseStorageTripData/'
```
Zu beachten ist die 1 Gigabyte Downloadgrenze pro Tag des kostenlosen Firebase Accounts.  Deswegen sollten neue Daten am besten immer zeitnah / regelmäßig sowie zum selben Pfad, gedownloaded werden.
#### Vorverarbeitung der Daten - data_import.py
Mit dem Script "data_import.py" werden die heruntergeladenen Daten vorverarbeitet. Dabei ist in diesem Script der komplette Prozess bishin zur Erstellung eines Trainingsdatensatzes, bestehend aus Features und Labeln von gebildeten Segmenten, enthalten.
Für die Vorverarbeitung wird eine .xlsx-Datei mit den Infrastrukturpunkten der Deutschen Bahn benötigt. Der Pfad zu dieser Datei wird in folgender Variable definiert. Die Datei findet sich in der Nextcloud und kann von dort lokal heruntergeladen werden. Der Pfad muss daraufhin angepasst werden.
```python
dbinfrastructure = pd.read_excel (r"***:\DB_Infrastructure.xlsx")
```
##### Einstellungen zur Vorverarbeitung
Einstellungen zur Vorverarbeitung können im Script "triplog_constants.py" getroffen werden. Dieses Script definiert verschiedene, allgemein benötigte Variablen.
Folgende Optionen können verändert werden, die Optionen sind den Kommentaren im Code zu entnehmen:
```python
# =============================================================================
# Data import and preperation - data_import.py
# =============================================================================

# VALIDATE = True: Check if data is consistant and delete, only needs to be
# used once after downloading new data
# VALIDATE = False: Do not check if data is consistant, can save time when
# data was already checked
VALIDATE = False

# Define with SECONDS_CUT_START and SECONDS_CUT_END how many seconds should be 
# cut at the beginning and the end of the raw data in seconds
# Define with SECONDS_SENSOR_SEGMENT how long a single segment is in seconds
SECONDS_CUT_START = 60
SECONDS_CUT_END = 60
SECONDS_SENSOR_SEGMENT = 60

# Write raw sensor data to files if you want to do time series analysation
# with this data (Be careful, this will accumulate many Gigabytes of data)
WRITE_SENSOR_DATA_TO_FILE = False

# Define the folder in which the initially generated training data is being
# saved in with SENSOR_DATA_SEGMENT_FOLDER
SENSOR_DATA_SEGMENT_FOLDER = "C:/Users/***/Desktop/SensorData/"

# Define the file names of the initially generated training data
SENSOR_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "sensorSegments.csv"
GPS_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "gpsSegments.csv"
FUSED_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "fusedSegments.csv"

# Define the used interpolation method for raw data resampling with
# INTERPOLATION_METHOD. Linear or spline interpolation is possible
INTERPOLATION_METHOD = 'linear'             # 'linear' or 'spline'

# Define the interpolation frequency for sensor data with INTERPOLATE_FREQUENCY
# in given format --> !!! See SENSOR_INTERPOLATE_FREQUENCY_INT !!! <--
INTERPOLATE_FREQUENCY = '20ms'              # Sensor resample frequency [s]
# Define the interpolation frequency for gps data with 
# GPS_INTERPOLATE_FREQUENCY in given format
GPS_INTERPOLATE_FREQUENCY = '1s'            # Gps resample frequency    [s]
# Define the interpolation frequency for sensor data with 
# SENSOR_INTERPOLATE_FREQUENCY_INT in Hz as Integer
SENSOR_INTERPOLATE_FREQUENCY_INT = 50       # Sensor resample frequency [Hz]

# Define if Google Speeds should be used for feature calculation instead of
# using recorded gps points to calculate speed and dependend features
USE_GOOGLE_SPEEDS = True
```
##### Anpassung der Datenquelle
Der Pfad der Quelldaten muss (im Script ganz unten, Z.928f.) angepasst werden. Sollen alle Daten verarbeitet werden, so muss der Ordner mit den vom "data_grabber" heruntergeladenen Dateien angegeben werden, siehe folgendes Beispiel:
```python
path = "Z:/***/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"
```
Soll die Prüf-/Referenzstrecke vorverarbeitet werden, so muss der Ordner, in welchem die beiden zugehörigen Dateien anstatt des anderen Ordners angegeben werden.
```python
path = "C:/***/***/***/SensorData/Testdaten/"
```

##### Benötigte Ordnerstruktur für das Speichern der erstellten Daten
Die vorverarbeiteten Daten werden in einem in "triplog_constants.py" festgelegten Ordner gespeichert. Dieser Ordner muss zuvor schon existieren (genau wie alle anderen Ordner), die Ordner werden nicht automatisch erstellt!
```python
# Define the folder in which the initially generated training data is being
# saved in with SENSOR_DATA_SEGMENT_FOLDER
SENSOR_DATA_SEGMENT_FOLDER = "C:/Users/***/***/SensorData/"
```

##### Dauer des Scripts
Die Ausführung des Script benötigt je nach Datenmenge mehrere Stunden (zuletzt 12-14 Stunden). Die Ausführung benötigt aufgrund der Berechnung des Features mit der DB Infrastruktur so lange.

