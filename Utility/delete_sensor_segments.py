# =============================================================================
# Löscht alle gespeicherten Sensor-Segmente aus dem in constants.py
# angegebenen Ordner
# https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
# =============================================================================     
import sys, shutil, os
sys.path.insert(0,'..')

import constants as C

folder = C.SENSOR_DATA_SEGMENT_FOLDER

if(__name__ == "__main__"):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            print("File could not be deleted")