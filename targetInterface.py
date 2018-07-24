import RPi.GPIO as GPIO

class TargetInterface ():
    def __init__ (self, t1_hit_handler, t2_hit_handler):
        
        GPIO.setmode(GPIO.BOARD)
        
        self.target1pins = [31, 29, 13, 15, 19]
        self.target2pins = [26, 24, 22, 18, 16]
        
        [GPIO.setup(pin, GPIO.IN) for pin in self.target1pins]
        [GPIO.setup(pin, GPIO.IN) for pin in self.target2pins]
        
        [GPIO.add_event_detect(pin, GPIO.FALLING, self.handle_hit) for pin in self.target1pins]
        [GPIO.add_event_detect(pin, GPIO.FALLING, self.handle_hit) for pin in self.target2pins]

        self.t1_hit_handler = t1_hit_handler
        self.t2_hit_handler = t2_hit_handler
        print('new target listener');

    def handle_hit(self, pin):
        print(pin);
        if pin in self.target1pins:
            self.t1_hit_handler
        if pin in self.target2pins:
            self.t2_hit_handler
