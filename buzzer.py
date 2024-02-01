import RPi.GPIO as GPIO
from time import sleep

# Disable warnings (optional)
GPIO.setwarnings(False)

# Select GPIO mode
GPIO.setmode(GPIO.BCM)

# Set buzzer - pin 16 as output
buzzer = 16
GPIO.setup(buzzer, GPIO.OUT)

def hidup():
    GPIO.output(buzzer, GPIO.HIGH)
    print("Beep")
    sleep(1.5)  # Buzzer sounds for 1.5 seconds

# def mati():
    # Turn off the buzzer
    GPIO.output(buzzer, GPIO.LOW)

    # Cleanup and exit the program
GPIO.cleanup()

# # Turn on the buzzer
# GPIO.output(buzzer, GPIO.HIGH)
# print("Beep")
# sleep(1.5)  # Buzzer sounds for 1.5 seconds

# # Turn off the buzzer
# GPIO.output(buzzer, GPIO.LOW)

# # Cleanup and exit the program
# GPIO.cleanup()
