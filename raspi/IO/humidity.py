#!/usr/bin/python3
import Adafruit_DHT
import time, threading

DHT_11 = 11
PIN = 26
frequency = 2

humidity, temperature = -1, -1


def read_sensor():
    global humidity, temperature
    humidity, temperature = Adafruit_DHT.read_retry(DHT_11, PIN)


def next_read():
    read_sensor()
    threading.Timer(frequency, next_read).start()

next_read()

if __name__ == "__main__":
    while True:
        read_sensor()
        print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
