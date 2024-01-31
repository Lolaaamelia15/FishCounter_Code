import RPi.GPIO as GPIO
from time import sleep

# Select GPIO mode
GPIO.setmode(GPIO.BCM)

#  Set waterpump - pin 23 as output 
waterpump = 23
GPIO.setup(waterpump, GPIO.OUT)

def on():
    GPIO.output(waterpump, GPIO.HIGH)
    sleep(1.5)

def off():
    GPIO.output(waterpump, GPIO.LOW)

    # Cleanup and exit the program
GPIO.cleanup()