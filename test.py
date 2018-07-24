#import GPIO
import RPi.GPIO as GPIO
import time

#use hw pin numbers
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.IN)

timestamp = time.time()

bounce_timeout = 0.3 #100 miliseconds
count = 0

def handle(pin):
    global timestamp, count, bounce_timeout
    time_now = time.time()
    print( time_now - timestamp )
    if ( time_now - timestamp ) > bounce_timeout:
        timestamp = time_now
        count = count+1
        print(count)
        print(pin)

GPIO.add_event_detect(13, GPIO.FALLING, handle)

handle(1)
time.sleep(30)
