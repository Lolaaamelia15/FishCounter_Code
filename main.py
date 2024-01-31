import requests
import json
import Counter
import time
from servo import Servo
import servo
import lcd_display
import waterpump
# import buzzer
import cProfile

servo = Servo()
waterpump.setup_gpio()

while(True):
    try:
        print("getting status..")
        x = requests.get('https://fishcounterta.000webhostapp.com/status.php')
        response_json = x.json()

        # Mengekstrak nilai dari JSON
        # id_value = response_json['id']
        hitung_status = response_json['hitung']

        if hitung_status == 'true':
            jumlah_value = int(response_json['jumlah'])
            harga_value = int(response_json['harga'])
            lcd_display.display(jumlah_value=jumlah_value,harga_value=harga_value*jumlah_value)

            # #buka servo
            servo.open()
            
            # hidupkan waterpump
            waterpump.on()
            
            # call hitung
            Counter.count(jumlah_value)

            # tutup servo dan bunyi buzzer
            servo.close()
            # buzzer.hidup()
            # print("beep")

            waterpump.off()

            # tampilkan data di lcd
            print(jumlah_value*harga_value)


            # # reset table status
            # x = requests.post('https://fishcounterta.000webhostapp.com/status.php') 
            # print(x.json())
    except KeyboardInterrupt:
        waterpump.off()
        servo.close()
        lcd_display.close()
        break
    except Exception as e:
        waterpump.off()
        servo.close()
        lcd_display.close()
        print(e.args)
    #     print(traceback.format)
    finally:
        # print(jumlah_value)
        time.sleep(3)

