#!/usr/bin/python3
import sys
import Adafruit_DHT

DHT_11 = 11
PIN = 26

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_11, 6)
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))