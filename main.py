import requests
import json
# import Counter
import newCounter
import time
from servo import Servo
import lcd_display
import waterpump
import buzzer
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

            # waterpump.on()              # Hidupkan waterpump
            jumlah_ikan = 0
            while (jumlah_ikan < jumlah_value):
                servo.close()             # Matikan servo
                jumlah_ikan += newCounter.count(interval=10) # call hitung
                servo.open()                # Hidupkan servo
                time.sleep(10) # waktu untuk mengeluarkan ikan
           
            # waterpump.off()           # Matikan waterpump
            buzzer.setup_gpio()
            buzzer.hidup()            # Bunyikan buzzer
            

            print(jumlah_value*harga_value) # Print harga total di terminal

            # reset table status
            x = requests.post('https://fishcounterta.000webhostapp.com/status.php') 
            print(x.json())

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
        time.sleep(3)

