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
def record_data(timeout_s, sensor_read_callback, ids):
    tic = time.time()
    df = None
    while time.time() - tic < timeout_s:
        timestamp, data = sensor_read_callback()

    return df


def write_image(image, ambiance):
    global i
    i+=1
    ambiance_path = os.path.join(log_path, ambiance)
    cv2.imwrite(os.path.join(ambiance_path, "{:0>2d}.png".format(i)), frame)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    write_image(frame, ambiance=ambiance[0])
    print(frame.shape)

    time.sleep(1)

##cap.release()
