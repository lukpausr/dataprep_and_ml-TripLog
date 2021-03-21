# =============================================================================
# KONSTANTEN
# =============================================================================
VALIDATE = False


SECONDS_CUT_START = 60
SECONDS_CUT_END = 60
SECONDS_SENSOR_SEGMENT = 30

WRITE_SENSOR_DATA_TO_FILE = False

SENSOR_DATA_SEGMENT_FOLDER = "C:/Users/Lukas/Desktop/SensorData/"
SENSOR_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "sensorSegments.csv"
GPS_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "gpsSegments.csv"
FUSED_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "fusedSegments.csv"

# INTERPOLATE_SIZE = 1000
INTERPOLATE_FREQUENCY = '20ms'              # [s]
GPS_INTERPOLATE_FREQUENCY = '1s'            # [s]
SENSOR_INTERPOLATE_FREQUENCY_INT = 50       # [Hz]

# =============================================================================
# Fast Fourier Transformation
# =============================================================================
SHOW_FFT_PLOTS = True
DATA_FREQUENCY_HZ = SENSOR_INTERPOLATE_FREQUENCY_INT
SAMPLE_POINTS = SECONDS_SENSOR_SEGMENT * DATA_FREQUENCY_HZ

# =============================================================================
# Fast Fourier Graphs Video Output
# =============================================================================
GRAPH_PICTURE_FOLDER = "C:/Users/Lukas/Desktop/Graphen"
VIDEO_DESTINATION_FOLDER = "C:/Users/Lukas/Desktop/"

# =============================================================================
# Hybrid Machine Learning
# =============================================================================
NORMALIZE_ELSE_STANDARDIZE = False
COMPRESS_LABELS = True
GENERATE_ELSE_LOAD_DATA = False
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
                                'sensor_varGyro'
                            ]
HYBRID_SELECTED_LABELS =    [
                                'Label', 
                                'Sublabel', 
                            ]
DATASET_FOLDER = SENSOR_DATA_SEGMENT_FOLDER + "dataset/"

# =============================================================================
# Start Program
# =============================================================================






