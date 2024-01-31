from RPLCD.i2c import CharLCD
import time

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

def display(jumlah_value=0, harga_value=0):
    lcd.clear()
    lcd.write_string("Jumlah: {} \r\nHarga: {}".format(jumlah_value, harga_value))

def close():
    lcd.clear()
    lcd.close()

