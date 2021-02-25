#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import numpy as np
import time
import cv2
from raspi.dataset_creation import log_path
from raspi.ambiance import ambiance

cap = cv2.VideoCapture(0)
i = 0


## TODO
## fonction enregistre pour un temps un nb de fichier dans le dossier
def record_data(timeout_s, target = 'none'):
    tic = time.time()
    while time.time() - tic < timeout_s:
      
      ret, frame = cap.read()
      data = write_image(frame, target())



def write_image(frame, ambiance):
    #global i
    #i+=1
    ambiance_path = os.path.join(log_path, ambiance)
    if not os.path.exists(ambiance_path):
      os.makedirs(ambiance_path)
    cv2.imwrite(os.path.join(ambiance_path, "{}.png".format(time.ctime())), frame)
    return

while True:
    # Capture frame-by-frame
    tic = time.time()
    
    ret, frame = cap.read()
    write_image(frame, ambiance=ambiance[0])
    #print(frame.shape)
    print(1/(time.time() - tic))
    #time.sleep(1)

cap.release()
