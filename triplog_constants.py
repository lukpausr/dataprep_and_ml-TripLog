# =============================================================================
# KONSTANTEN
# =============================================================================
VALIDATE = True


SECONDS_CUT_START = 60
SECONDS_CUT_END = 60
SECONDS_SENSOR_SEGMENT = 60

WRITE_SENSOR_DATA_TO_FILE = False

SENSOR_DATA_SEGMENT_FOLDER = "C:/Users/Lukas/Desktop/SensorData/"
SENSOR_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "sensorSegments.csv"
GPS_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "gpsSegments.csv"
FUSED_DATA_CSV = SENSOR_DATA_SEGMENT_FOLDER + "fusedSegments.csv"

INTERPOLATE_FREQUENCY = '20ms'              # [s]
GPS_INTERPOLATE_FREQUENCY = '1s'            # [s]
SENSOR_INTERPOLATE_FREQUENCY_INT = 50       # [Hz]

USE_GOOGLE_SPEEDS = True
# =============================================================================
# Fast Fourier Transformation
# =============================================================================
SHOW_FFT_PLOTS = False
DATA_FREQUENCY_HZ = SENSOR_INTERPOLATE_FREQUENCY_INT
SAMPLE_POINTS = SECONDS_SENSOR_SEGMENT * DATA_FREQUENCY_HZ

# =============================================================================
# Fast Fourier Graphs Video Output
# =============================================================================
GRAPH_PICTURE_FOLDER = "C:/Users/Lukas/Desktop/Graphen"
VIDEO_DESTINATION_FOLDER = "C:/Users/Lukas/Desktop/"

# =============================================================================
# Hybrid Machine Learning Visualisation
# =============================================================================
CLEAN_LABELS =  [
                    ['Car_Hybrid',          'Hybridauto'    ],
                    ['Car_Conventional',    'Auto'          ],
                    ['Car_Electric',        'Elektroauto'   ],
                    ['Foot_Walking',        'Gehen'         ],
                    ['Foot_Running',        'Joggen'        ],
                    ['Train_Suburban',      'S-Bahn'        ],
                    ['Train_City',          'U-Bahn'        ],
                    ['Bike_Conventional',   'Fahrrad'       ],
                    ['Bike_Electric',       'e-Bike'        ],
                    ['Bus_Conventional',    'Bus'           ]
                ]
CLEAN_UNITS =   [
                    ['avgSpeed',            '$m/s$'           ], 
                    ['maxSpeed',            '$m/s$'           ],             
                    ['minAcc',              '$m/s^2$'       ], 
                    ['maxAcc',              '$m/s^2$'       ], 
                    ['tow',                 '$s$'             ], 
                    ['towAvgSpeed',         '$s$'             ], 
                    ['maxFreqACC',          '$Hz$'            ],
                    ['maxFreqGYRO',         '$Hz$'            ],
                    ['maxSingleFreqACC',    '$Hz$'            ],
                    ['maxSingleFreqGYRO',   '$Hz$'            ],
                    ['stdSpeed',            '$m/s$'           ], 
                    ['varSpeed',            '$(m/s)^2$'       ], 
                    ['stdAcc',              '$m/s^2$'       ], 
                    ['varAcc',              '$m/(s^2)^2$'   ],
                    ['sensor_stdAcc',       '$Hz$'            ], 
                    ['sensor_varAcc',       '$Hz^2$'          ], 
                    ['sensor_stdGyro',      '$Hz$'            ], 
                    ['sensor_varGyro',      '$Hz^2$'          ]
                ]
# =============================================================================
# Hybrid Machine Learning
# =============================================================================
NORMALIZE_ELSE_STANDARDIZE = True
COMPRESS_LABELS = False
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
OFFLINE_TEST_PATH_GPS = r"C:\Users\Lukas\Desktop\1617195745679_Scooter_Electric_GPS.csv"
OFFLINE_TEST_SEGMENTS = "C:/Users/Lukas/Desktop/SensorData/Testdaten/fusedSegments.csv"
# =============================================================================
# Start Program
# =============================================================================






