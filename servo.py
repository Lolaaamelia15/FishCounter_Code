import pigpio

class Servo:
    def __init__(self) -> None:
        print("Initialize Servo")
        self.pi = pigpio.pi()
        self.servoPin = 18
        self.pi.set_servo_pulsewidth(self.servoPin, 0)

    def open(self):
        print("Pintu Terbuka")
        self.pi.set_servo_pulsewidth(self.servoPin, 2500)

    def close(self):
        print("Pintu Tertutup")
        self.pi.set_servo_pulsewidth(self.servoPin, 500)

    def stop(self):
        print("Stop Servo")
        self.pi.set_servo_pulsewidth(self.servoPin, 0)
        self.pi.stop()