import RPi.GPIO as GPIO
import time

# Pilih pin yang sesuai dengan konfigurasi hardware Anda
pin = 26

GPIO.setmode(GPIO.BCM) # Gunakan nomor pin BCM
GPIO.setup(pin, GPIO.OUT) # Set pin sebagai output

# try:
#   while True:
#       # Aktifkan relay
#       GPIO.output(pin, GPIO.HIGH)
#       print("RELAY: on")
#       time.sleep(1)

#       # Matikan relay
#       GPIO.output(pin, GPIO.LOW)
#       print("RELAY: off")
#       time.sleep(2)
# except KeyboardInterrupt:
#   pass
# finally:
#   GPIO.cleanup()

def aktifkan():
  GPIO.output(pin, GPIO.HIGH)
  print("Relay : On")
  time.sleep(1)

def matikan():
  GPIO.output(pin, GPIO.LOW)
  print("Relay : Of")
  time.sleep(1)

GPIO.cleanup()


