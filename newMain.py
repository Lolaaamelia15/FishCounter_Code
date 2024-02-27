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

video_opened = False

while(True):
    try:
        print("getting status..")
        x = requests.get('https://fishcounterta.000webhostapp.com/status.php')
        response_json = x.json()

        # Mengekstrak nilai dari JSON
        hitung_status = response_json['hitung']

        if hitung_status == 'true':
            jumlah_value = int(response_json['jumlah'])
            harga_value = int(response_json['harga'])
            lcd_display.display(jumlah_value=jumlah_value,harga_value=harga_value*jumlah_value)

            if not video_opened:
                video.open(1)  # Buka kamera
                video_opened = True

            jumlah_ikan = 0
            while (jumlah_ikan < jumlah_value):
                servo.close()  # Matikan servo
                # Panggil fungsi count untuk menghitung jumlah ikan dalam interval tertentu
                jumlah_ikan = newCounter.count(interval=10)
                servo.open()   # Hidupkan servo
                time.sleep(10) # Waktu untuk mengeluarkan ikan
           
            buzzer.setup_gpio()
            buzzer.hidup()   # Bunyikan buzzer

            print(jumlah_value*harga_value)  # Print harga total di terminal

            # Reset table status
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
        
    finally:
        time.sleep(3)
