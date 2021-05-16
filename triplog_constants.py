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
SENSOR_DATA_SEGMENT_FOLDER = "C:/Users/***/***/SensorData/"

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



# =============================================================================
# Fast Fourier Transformation
# =============================================================================

# Define if fft (fast fourier transformation) results should be plotted
SHOW_FFT_PLOTS = False

# Define frequency of sensor data (dependend 
# on SENSOR_INTERPOLATE_FREQUENCY_INT so no need to change this constant)
DATA_FREQUENCY_HZ = SENSOR_INTERPOLATE_FREQUENCY_INT
# Define number of sample points (dependend on SECONDS_SENSOR_SEGMENT and
# DATA_FREQUENCY_HZ so no need to change this constant)
SAMPLE_POINTS = SECONDS_SENSOR_SEGMENT * DATA_FREQUENCY_HZ



# =============================================================================
# Fast Fourier Graphs Video Output
# CURRENTLY NOT IMPLEMENTED - CHANGING VALUES DO NOT HAVE INFLUENCE ON RESULTS
# =============================================================================
GRAPH_PICTURE_FOLDER = "C:/Users/***/Desktop/Graphen"
VIDEO_DESTINATION_FOLDER = "C:/Users/***/Desktop/"



# =============================================================================
# Hybrid Machine Learning Visualisation
# =============================================================================

# Define clean labels which can be used instead of complicated predefined
# labels
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
# Define clean labels for reduced label visualisation to replace english labels
CLEAN_SHORT_LABELS =    [
                            ['Car',     'Auto'      ],
                            ['Foot',    'Fuß'       ],
                            ['Train',   'Zug'       ],
                            ['Bike',    'Fahrrad'   ],
                            ['Bus',     'Bus'       ]
                        ]
# Defines units for different used features
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
                    ['sensor_varGyro',      '$Hz^2$'          ],
                    ['meanNearestInfrastructure', '$m$'     ]
                ]
# Defines colors for each type of transportation for the created maps 
CLEAN_COLORS =  [
                    ['Hybridauto',      'lightred'      ],
                    ['Auto',            'red'           ],
                    ['Elektroauto',     'pink'          ],
                    ['Gehen',           'green'         ],
                    ['Joggen',          'black'         ],
                    ['S-Bahn',          'blue'          ],
                    ['U-Bahn',          'lightblue'     ],
                    ['Fahrrad',         'yellow'        ],
                    ['e-Bike',          'lightgreen'    ],
                    ['Bus',             'orange'        ]
                ]
# Defines colors for each type of transportation for the created maps for
# usage with reduced labels
CLEAN_SHORT_COLORS =    [
                            ['Auto',        'red'      ],
                            ['Fuß',         'green'    ],
                            ['Zug',         'blue'     ],
                            ['Fahrrad',     'yellow'   ],
                            ['Bus',         'orange'   ]
                        ]



# =============================================================================
# Hybrid Machine Learning - hybrid_ml.py
# =============================================================================

# Define if data should be normalized or standardized. Data needs to be
# regenerated if this value is changed
NORMALIZE_ELSE_STANDARDIZE = True

# Define if models should be trained with compressed labels or with
# uncompressed labels. Data DOESNT need to be regenerated if this value is
# changed
COMPRESS_LABELS = True

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
OFFLINE_TEST_PATH_GPS = r"***:\Users\***\1617195745679_Scooter_Electric_GPS.csv"
s
# Define location of the segmented and feature calculated reference track file
# This data needs to created by using data_import.py to calculate features
# once and can then be used to make predictions
OFFLINE_TEST_SEGMENTS = "***:/Users/***/SensorData/Testdaten/fusedSegments.csv"