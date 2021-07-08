#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QSlider, QStyleFactory, QVBoxLayout, QFrame)
from thonny.plugins.microbit.api_stubs.builtins import frozenset

import dataset_creation as ds
import sensor
from ambiance import ambiance
from raspi.IO import camera

label_ambianceType = ambiance
color = ["green", "yellow", "orange", "red"]
ambianceType = 1
ambianceLevel = 50


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        mainLayout = QVBoxLayout()
        # TopLayout
        topLayout = QHBoxLayout()
        self.ambianceLevel = QProgressBar()
        self.ambianceLevel.setOrientation(Qt.Vertical)
        self.ambianceLevel.setValue(ambianceLevel)
        self.ambianceLevel.setAlignment(Qt.AlignCenter)
        topLayout.addWidget(self.ambianceLevel)

        self.ambianceType = QLabel()
        self.ambianceType.setText(label_ambianceType[ambianceType])
        self.ambianceType.setStyleSheet("background-color: {}".format(color[ambianceType]))
        topLayout.addWidget(self.ambianceType)

        # Camera feedback
        self.camera = QLabel()
        self.camera.setPixmap(QPixmap("log/Thu Feb 25 12:54:37 2021/R/57.png"))
        topLayout.addWidget(self.camera)

        mainLayout.addLayout(topLayout)

        self.sensor_value = QLabel(text="...")
        mainLayout.addWidget(self.sensor_value)

        # Bottom layout
        bottomLayout = QHBoxLayout()
        recordLayout = QVBoxLayout()

        self.record_timeout = QLineEdit()
        recordLayout.addWidget(self.record_timeout)

        self.start_recording = QPushButton(text="Record")
        self.start_recording.clicked.connect(self.start_recording_fn)
        recordLayout.addWidget(self.start_recording)

        self.info = QLabel(text="Waiting")
        recordLayout.addWidget(self.info)
        self.log = QLabel(text="...")
        recordLayout.addWidget(self.log)

        bottomLayout.addLayout(recordLayout)
        bottomLayout.addWidget(QFrame(frameShape=QFrame.VLine))

        # Left pane
        leftLayout = QHBoxLayout()
        bottomLeftText = QLabel("Phako")
        leftLayout.addWidget(bottomLeftText)
        self.slider_ambianceType = QSlider(orientation=Qt.Vertical)
        self.slider_ambianceType.setValue(ambianceLevel)
        self.slider_ambianceType.setTickInterval(10)
        self.slider_ambianceType.setTickPosition(QSlider.TicksBothSides)
        self.slider_ambianceType.sliderMoved.connect(lambda: self.setAmbianceLevel(self.slider_ambianceType.value()))
        self.slider_ambianceType.sliderReleased.connect(lambda: self.setAmbianceLevel(self.slider_ambianceType.value()))
        leftLayout.addWidget(self.slider_ambianceType)
        bottomLayout.addLayout(leftLayout)

        # Right pane
        rightLayout = QVBoxLayout()
        self.bt_0 = QPushButton(text="R")
        self.bt_0.setStyleSheet("background-color: green")
        self.bt_0.clicked.connect(lambda: self.setAmbianceType(0))
        self.bt_1 = QPushButton(text="Ambiance Moyenne")
        self.bt_1.setStyleSheet("background-color: yellow")
        self.bt_1.clicked.connect(lambda: self.setAmbianceType(1))
        self.bt_2 = QPushButton(text="Bonnes idées")
        self.bt_2.setStyleSheet("background-color: orange")
        self.bt_2.clicked.connect(lambda: self.setAmbianceType(2))
        self.bt_3 = QPushButton(text="Grosse Soirée")
        self.bt_3.setStyleSheet("background-color: red")
        self.bt_3.clicked.connect(lambda: self.setAmbianceType(3))
        rightLayout.addWidget(self.bt_3)
        rightLayout.addWidget(self.bt_2)
        rightLayout.addWidget(self.bt_1)
        rightLayout.addWidget(self.bt_0)
        bottomLayout.addLayout(rightLayout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Styles")
        QApplication.setStyle(QStyleFactory.create("Fusion"))

    def setAmbianceLevel(self, new_ambianceLevel):
        global ambianceLevel
        ambianceLevel = new_ambianceLevel
        self.ambianceLevel.setValue(ambianceLevel)
        # self.slider_ambianceType.setValue(ambianceLevel)

    def setAmbianceType(self, new_ambianceType):
        global ambianceType
        ambianceType = new_ambianceType
        self.ambianceType.setStyleSheet("background-color: {}".format(color[ambianceType]))
        self.ambianceType.setText(label_ambianceType[ambianceType])

    def getAmbianceLevel(self):
        global ambianceType
        return ambianceLevel

    def getAmbianceType(self):
        global ambianceLevel
        return ambianceType

    def start_recording_fn(self):
        timeout_s = int(self.record_timeout.text()) * 60
        self.info.setText("Start recording for {} minutes".format(timeout_s / 60))
        print("Start recording for {} minutes".format(timeout_s / 60))

        # Create Threads for sensors & camera
        sensor_record_thread = threading.Thread(
            target=
            lambda: ds.record_and_save(
                ds.record_data(
                    timeout_s,
                    sensor.read_all_sensor,
                    ["Humidity", "Temperature", "Motion"],
                    self.update_sensor,
                    (self.getAmbianceLevel, self.getAmbianceType),
                    ["AmbianceLevel", "AmbianceType"]
                )
            ))
        camera_record_thread = threading.Thread(
            target=lambda: camera.record_data(timeout_s, target=self.getAmbianceType, update=self.update_camera)
        )

        # Start Thread
        camera_record_thread.start()
        sensor_record_thread.start()
        self.log.setText("Record will be saved in {}".format(ds.log_path))

    def update_sensor(self):
        from IO.humidity import humidity, temperature
        from IO.motion import state
        str = 'Temp: {0:0.1f} C , Humidity: {1:0.1f}%, Motion: {2}'.format(temperature, humidity, state)
        self.sensor_value.setText(str)

    def update_camera(self, frame):
        height, width, depth = frame.shape
        self.camera.setPixmap(QPixmap(QImage(frame.data, width, height, QImage.Format_RGB888)))

    # def next_sensor_print(self):
    #     self.update_sensor()
    #     threading.Timer(frequency, next_read).start()
    #
    # next_read()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
