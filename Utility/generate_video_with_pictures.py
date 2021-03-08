import sys, shutil, os
sys.path.insert(0,'..')
import triplog_constants as C

import cv2
import numpy as np
import glob

frameSize = (1170, 604)

out = cv2.VideoWriter(C.VIDEO_DESTINATION_FOLDER + "output_video.avi", cv2.VideoWriter_fourcc(*'DIVX'), 20, frameSize)

for filename in glob.glob(C.GRAPH_PICTURE_FOLDER + '*.png'):
    img = cv2.imread(filename)
    out.write(img)

out.release()