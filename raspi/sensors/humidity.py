#!/usr/bin/python3
import Adafruit_DHT

DHT_11 = 11
PIN = 26

def read_sensor():
    global humidity, temperature
    humidity, temperature = Adafruit_DHT.read_retry(DHT_11, PIN)
    return [humidity, temperature]


if __name__ == "__main__":
    while True:
        read_sensor()
        print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
