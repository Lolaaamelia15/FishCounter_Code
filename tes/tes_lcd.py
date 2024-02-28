# from RPLCD.i2c import CharLCD

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
# lcd.clear()

# lcd.write_string('Hello, Wooooorld')

# from servo import Servo
# from time import sleep
# servo = Servo()
# servo.open()
# sleep(5)
# servo.close()
# sleep(5)
# servo.stop()

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.HIGH)
sleep(10)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.cleanup()