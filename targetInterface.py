import RPi.GPIO as GPIO
import time
import requests

class HttpBrainyInterface():
    def __init__(self):
        self.url = 'http://localhost:5000/target'

    def postEvent(self, targetId, pinIndex):
        r = requests.post(self.url, data={'targetId': targetId, 'pinIndex': pinIndex})

class TargetInterface ():
    def __init__ (self, pinList, targetId):
        self.pins = pinList;
        self.targetId = targetId;
        
        GPIO.setmode(GPIO.BOARD)
        [GPIO.setup(pin, GPIO.IN) for pin in self.pins]
        [GPIO.add_event_detect(pin, GPIO.FALLING, self.handle_hit) for pin in self.pins]

        self.timestamp = time.time()
        self.bounce_timeout = 0.3 #100 miliseconds

        self.webIF = HttpBrainyInterface();

    def handle_hit(self, pin):
        time_now = time.time()
        if ( time_now - self.timestamp ) > self.bounce_timeout:
            self.timestamp = time_now
            #emit hit
            self.webIF.postEvent(self.targetId, self.pins.index(pin));


if __name__ == '__main__':
    target0 = TargetInterface ([31, 13, 29, 15, 19], 0);
    target1 = TargetInterface ([16, 26, 18, 24, 22], 1);
    while True:
        time.sleep(9999)
