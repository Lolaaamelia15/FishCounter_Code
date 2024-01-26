# from RPLCD.i2c import CharLCD

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
# lcd.clear()

# lcd.write_string('Hello, World')

from servo import Servo
from time import sleep
servo = Servo()
servo.open()
sleep(5)
servo.close()
sleep(5)
servo.stop()