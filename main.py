import requests
import json
import Counter
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

            servo.open()                # Hidupkan servo 
            waterpump.on()              # Hidupkan waterpump
            
            Counter.count(jumlah_value) # call hitung
           
            servo.close()             # Matikan servo
            waterpump.off()           # Matikan waterpump
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

