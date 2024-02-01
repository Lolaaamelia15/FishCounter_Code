import RPi.GPIO as GPIO
from time import sleep

# Disable warnings (optional)
GPIO.setwarnings(False)

waterpump = 23
def setup_gpio():
    try:
        # Periksa apakah GPIO sudah diatur sebelumnya
        if GPIO.getmode() is None:
            # Jika belum, atur mode GPIO
            GPIO.setmode(GPIO.BCM)

        # Set water pump - pin 23 as output 
        # waterpump = 23
        GPIO.setup(waterpump, GPIO.OUT)

        return True
    except Exception as e:
        print(f"Error setting up GPIO: {e}")
        return False

# # Select GPIO mode
# GPIO.setmode(GPIO.BCM)

# #  Set waterpump - pin 23 as output 
# waterpump = 23
# GPIO.setup(waterpump, GPIO.OUT)

def on():
    GPIO.output(waterpump, GPIO.HIGH)
    # sleep(5)

def off():
    GPIO.output(waterpump, GPIO.LOW)

    # Cleanup and exit the program
# GPIO.cleanup()

# Periksa apakah pengaturan GPIO berhasil sebelum melanjutkan
if setup_gpio():
    # Contoh penggunaan
    try:
        on()  # Nyalakan pompa air selama 5 detik
        sleep(2)
        off()  # Matikan pompa air
    except KeyboardInterrupt:
        # Tangani interrupt keyboard (Ctrl+C)
        pass
    finally:
        # Pastikan pembersihan GPIO dilakukan sebelum keluar
        GPIO.cleanup()