from RPLCD.i2c import CharLCD
import time

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

def display(jumlah_value, harga_value):
    # jumlah_value = jumlah
    # harga_value= harga

    lcd.write_string("Jumlah: {} \r\nHarga: {}".format(jumlah_value, harga_value))
    # lcd.write_string(harga_text)
    # lcd.lf()
    #lcd.write_string(harga_text)
    time.sleep(10)
    lcd.clear()

lcd.close()

