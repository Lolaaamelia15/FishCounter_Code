import RPi.GPIO as GPIO
from time import sleep

# Disable warnings (optional)
GPIO.setwarnings(False)

# Select GPIO mode
GPIO.setmode(GPIO.BCM)

# Set buzzer - pin 23 as output
buzzer = 16
GPIO.setup(buzzer, GPIO.OUT)

def hidup():
    GPIO.output(buzzer, GPIO.HIGH)
    print("Beep")
    sleep(2) 
    GPIO.output(buzzer, GPIO.LOW)

# Cleanup and exit the program
GPIO.cleanup()

# Periksa apakah pengaturan GPIO berhasil sebelum melanjutkan
if setup_gpio():
    try:
        hidup()  # Nyalakan buzzer selama 2 detik
        sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        # Pastikan pembersihan GPIO dilakukan sebelum keluar
        GPIO.cleanup()