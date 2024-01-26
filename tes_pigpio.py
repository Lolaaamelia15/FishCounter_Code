# from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero import AngularServo
# from time import sleep

# factory = PiGPIOFactory()
# servo = AngularServo(18, pin_factory=factory, min_angle=0, max_angle=180)

# while True:
#     print("Max")
#     servo.max()
#     sleep(2)
#     print("Min")
#     servo.min()
#     sleep(2)

import pigpio
from time import sleep

pi = pigpio.pi()

servoPin = 18
pi.set_servo_pulsewidth(servoPin, 0)

try:
    while True:
        print("180")
        pi.set_servo_pulsewidth(servoPin, 2500)
        sleep(10)
        print("0")
        pi.set_servo_pulsewidth(servoPin, 500)
        sleep(2)
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(servoPin, 0)
    pi.stop()