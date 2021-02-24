#!/usr/bin/python3
import Adafruit_DHT
import time, threading

DHT_11 = 11
PIN = 26
frequency = 2

humidity, temperature = -1, -1


def read_sensor():
    global humidity, temperature
    temp_humidity, temp_temperature = Adafruit_DHT.read_retry(DHT_11, PIN)
    if 20 < temp_humidity < 100:
        humidity = temp_humidity
    if 0 < temp_temperature < 50:
        temperature = temp_temperature


def next_read():
    read_sensor()
    threading.Timer(frequency, next_read).start()

next_read()

if __name__ == "__main__":
    while True:
        read_sensor()
        print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
