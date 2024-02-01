import RPi.GPIO as GPIO
from time import sleep

# Disable warnings (optional)
GPIO.setwarnings(False)

buzzer = 24
def setup_gpio():
    try:
        # Periksa apakah GPIO sudah diatur sebelumnya
        if GPIO.getmode() is None:
            # Jika belum, atur mode GPIO
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer, GPIO.OUT)
        return True
    except Exception as e:
        print(f"Error setting up GPIO: {e}")
        return False

def hidup():
    GPIO.output(buzzer, GPIO.HIGH)
    print("Beep")
    sleep(3) 
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