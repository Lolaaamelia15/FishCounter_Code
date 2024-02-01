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

        # Set water pump - pin 23 as output 
        # waterpump = 23
        GPIO.setup(buzzer, GPIO.OUT)

        return True
    except Exception as e:
        print(f"Error setting up GPIO: {e}")
        return False

# # Select GPIO mode
# GPIO.setmode(GPIO.BCM)

# # Set buzzer - pin 16 as output
# buzzer = 24 
# GPIO.setup(buzzer, GPIO.OUT)

def hidup():
    GPIO.output(buzzer, GPIO.HIGH)
    print("Beep")
    sleep(4)  # Buzzer sounds for 1.5 seconds

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

# Periksa apakah pengaturan GPIO berhasil sebelum melanjutkan
if setup_gpio():
    # Contoh penggunaan
    try:
        hidup()  # Nyalakan pompa air selama 5 detik
        sleep(2)
    except KeyboardInterrupt:
        # Tangani interrupt keyboard (Ctrl+C)
        pass
    finally:
        # Pastikan pembersihan GPIO dilakukan sebelum keluar
        GPIO.cleanup()