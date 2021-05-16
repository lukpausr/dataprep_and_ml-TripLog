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
Die erstellten Daten werden unter den Bezeichnungen "sensorSegments.csv", "gpsSegments.csv" und "fusedSegments.csv" gespeichert und müssen nachträglich manuell getrennt werden. Die Ordnerstruktur, die für das Machine Learning benötigt, wird zu einem späteren Zeitpunkt in dieser Anleitung erläutert. Zurzeit beinhaltet nur die Datei "fusedSegments.csv" nutzbare Daten. In den anderen Dateien werden (da Sie nicht benötigt werden) nicht alle dem jeweiligen Sensor zuzuordnenden Features abgelegt. Das Script "data_import.py" müsste dazu zunächst ergänzt werden.

##### Dauer des Scripts
Die Ausführung des Script benötigt je nach Datenmenge mehrere Stunden (zuletzt 12-14 Stunden). Die Ausführung benötigt aufgrund der Berechnung des Features mit der DB Infrastruktur so lange.

### Machine Learning
#### Machine Learning (Erstellung von Trainings- und Testdatensets) - hybrid_ml.py
Damit das Machine Learning Skript "hybrid_ml.py" zur Erstellung von Trainings- und Testdaten genutzt werden kann, müssen folgende Einstellungen in der Datei "triplog_constants.py" getroffen werden:
```python
# =============================================================================
# Hybrid Machine Learning - hybrid_ml.py
# =============================================================================

# Define if data should be normalized or standardized. Data needs to be
# regenerated if this value is changed
NORMALIZE_ELSE_STANDARDIZE = True

# Define if data should be (re)generated or loaded. At regeneration, no machine
# learning model training will take place. When set to False, models will be
# trained and evaluated
GENERATE_ELSE_LOAD_DATA = True

# Define in which folder the generated train- and testdata is being saved
DATASET_FOLDER = SENSOR_DATA_SEGMENT_FOLDER + "dataset/"
```
Der Pfad DATASET_FOLDER bestimmt, wo die erstellten Trainings- und Testdatensets gespeichert werden. Sie werden beim Trainieren der Machine Learning Modelle automatisch wieder eingelesen.
Die Normalisierung oder Standardisierung findet bereits bei der Erstellung der Datensets statt und muss deshalb schon an dieser Stelle erfolgen.

#### Machine Learning (Modelltraining und Evaluation ) - hybrid_ml.py
Für das Trainieren der verschiedenen Machine Learning Modelle und der Evaluation dieser (+ Referenzstreckenvisualisierung) müssen im Script "triplog_constants.py" folgende Einstellungen getätigt werden:
```python
# =============================================================================
# Hybrid Machine Learning - hybrid_ml.py
# =============================================================================

# Define if data should be normalized or standardized. Data needs to be
# regenerated if this value is changed
NORMALIZE_ELSE_STANDARDIZE = True

# Define if models should be trained with compressed labels or with
# uncompressed labels. Data DOESNT need to be regenerated if this value is
# changed
COMPRESS_LABELS = False

# Define if data should be (re)generated or loaded. At regeneration, no machine
# learning model training will take place. When set to False, models will be
# trained and evaluated
GENERATE_ELSE_LOAD_DATA = False

# Defines which features will be used for the training of the machine learning
# models
HYBRID_SELECTED_FEATURES = [
                                'avgSpeed', 
                                'maxSpeed', 
                                'minAcc', 
                                'maxAcc', 
                                'tow', 
                                'towAvgSpeed', 
                                'maxFreqACC',
                                'maxFreqGYRO',
                                'maxSingleFreqACC',
                                'maxSingleFreqGYRO',
                                'stdSpeed', 
                                'varSpeed', 
                                'stdAcc', 
                                'varAcc',
                                'sensor_stdAcc', 
                                'sensor_varAcc', 
                                'sensor_stdGyro', 
                                'sensor_varGyro',
                                'meanNearestInfrastructure'
                            ]

# Defines which depth of labels should be used to generate models, please use
# COMPRESS_LABELS to achieve reduced label training of models
HYBRID_SELECTED_LABELS =    [
                                'Label', 
                                'Sublabel', 
                            ]

# Define in which folder the generated train- and testdata is being saved
DATASET_FOLDER = SENSOR_DATA_SEGMENT_FOLDER + "dataset/"

# Define location of the raw reference track file
OFFLINE_TEST_PATH_GPS = r"C:\Users\***\1617195745679_Scooter_Electric_GPS.csv"

# Define location of the segmented and feature calculated reference track file
# This data needs to created by using data_import.py to calculate features
# once and can then be used to make predictions
OFFLINE_TEST_SEGMENTS = "C:/Users/***/SensorData/Testdaten/fusedSegments.csv"
```
Die Standardisierung / Normalisierung muss dabei diesselbe sein, wie beim Erstellen der Datensets, da diese Einstellung Einfluss auf das Einlesen der Referenstrecke und deren Vorhersagen hat. Mit COMPRESS_LABELS kann entschieden werden, welche Labeltiefe beim Trainieren der Modelle verwendet wird. GENERATE_ELSE_LOAD_DATA muss auf False eingestellt sein, da sonst kein Machine Learning stattfinden wird. In HYBRID_SELECTED_FEATURES kann definiert werden (durch auskommentieren), welche Features für das Training benutzt werden. In OFFLINE_TEST_PATH_GPS wird der Quell-GPS-Pfad der Referenzstrecke hinterlegt, in OFFLINE_TEST_SEGMENTS wird das Dokument "fusedSegments.csv" mit den vorverarbeitenden Daten der Referenzstrecke hinterlegt. Diese Daten müssen zuvor mit "data_import.py" erstellt und gesondert abgespeichert werden.

#### Weitere Optionen
Weitere Optionen, Visualisierungen etc. können durch aus- und einkommentieren von relevanten Codeschnipseln im Quellcode aktiviert oder deaktiviert werden. Hierbei kann gerne experimentiert werden, die Laufzeit beim Trainieren der Modelle hält sich in Grenzen (wenige Minuten, wenn überhaupt).
Zum jetztigen Zeitpunkt werden die erstellten Modelle nicht lokal gespeichert sondern bei jedem Durchlauf erneut trainiert.

### Erstellte Trainings- und Testdatensets sowie Referenzstrecken
Bereits erstellte Trainings- und Testdatensets finden sich auf der Nextcloud (08-Datensets_fuer_Machine_Learning). Diese können für den Machine Learning Prozess lokal gespeichert und anschließend verwendet werden. Hierdurch entfällt die Zeitintensive Datenvorverarbeitung mit "data_import.py"
