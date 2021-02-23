import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 19
GPIO.setup(PIR_PIN, GPIO.IN)

print('Starting up the PIR Module (click on STOP to exit)')
time.sleep(1)
print('Ready-')

state = 0

def callback(pin):
    global state
    state = GPIO.input(pin)

GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(PIR_PIN, callback)  # assign function to GPIO PIN, Run function on change

# infinite loop
if __name__ == "__main__":
    while True:
        time.sleep(1)
        print(state)