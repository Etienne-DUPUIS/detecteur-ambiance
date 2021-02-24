#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time
import cv2

cap = cv2.VideoCapture(0)

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Save the frame
    cv2.imwrite('frame.png', frame)
    print(frame.shape)

    time.sleep(1)

##cap.release()
