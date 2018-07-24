#import GPIO
import RPi.GPIO as GPIO

#use hw pin numbers
GPIO.setmode(GPIO.BOARD)

#Target 1
T1_1 = 31
T1_2 = 29
T1_3 = 13
T1_4 = 15
T1_5 = 19

#Target 2
T2_1 = 26
T2_2 = 24
T2_3 = 22
T2_4 = 18
T2_5 = 16

GPIO.setup([T1_1, T1_2, T1_3, T1_4, T1_5, T2_1, T2_2, T2_3, T2_4, T2_5], GPIO.IN)

class TargetInterface ():
    def __init__ (self, t1_hit_handler, t2_hit_handler):
        GPIO.add_event_detect(T1_1, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T1_2, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T1_3, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T1_4, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T1_5, GPIO.FALLING, t1_hit_handler)

        GPIO.add_event_detect(T2_1, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T2_2, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T2_3, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T2_4, GPIO.FALLING, t1_hit_handler)
        GPIO.add_event_detect(T2_5, GPIO.FALLING, t1_hit_handler)
