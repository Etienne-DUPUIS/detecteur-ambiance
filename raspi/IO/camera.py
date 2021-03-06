#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

import cv2

from raspi.ambiance import ambiance
from raspi.dataset_creation import log_path

cap = cv2.VideoCapture(0)
i = 0


## TODO
## fonction enregistre pour un temps un nb de fichier dans le dossier
def record_data(timeout_s, target='none', update=None):
    tic = time.time()
    while time.time() - tic < timeout_s:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        update(frame)
        write_image(frame, ambiance[target()])


def write_image(frame, ambiance):
    # global i
    # i+=1
    ambiance_path = os.path.join(log_path, ambiance)
    if not os.path.exists(ambiance_path):
        os.makedirs(ambiance_path)
    cv2.imwrite(os.path.join(ambiance_path, "{}.png".format(time.ctime())), frame)


if __name__ == '__main__':
    while True:
        # Capture frame-by-frame
        tic = time.time()

        ret, frame = cap.read()
        write_image(frame, ambiance=ambiance[0])
        # print(frame.shape)
        print(1 / (time.time() - tic))
        # time.sleep(1)
    cap.release()
