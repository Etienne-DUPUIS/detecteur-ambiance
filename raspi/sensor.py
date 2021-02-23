from sensors import humidity, motion
from datetime import datetime

class Sensor():
    def read(self):
        pass


class DHT(Sensor):
    def read(self):
        return [humidity.humidity, humidity.temperature]


class PIR(Sensor):
    def read(self):
        return motion.state


# Instanciate sensors
DHT11 = DHT()
PIR01 = PIR()
Sensor_list = [
    DHT11,
    PIR01
]


# Method to read them all
def read_all_sensor():
    result = []
    for sensor in Sensor_list:
        read_all = sensor.read()
        if not isinstance(read_all, list):
            read_all = [read_all]
        for sensor_value in read_all:
            result.append(sensor_value)
    return datetime.now().ctime(), result


while True:
    print(read_all_sensor())
