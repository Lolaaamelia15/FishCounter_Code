# import Counter
# import servo
# import lcd_display
# import relay


# servo.init()
# # servo.buka()
# # relay.aktifkan()
# Counter.count(1)
# # servo.tutup()
# # relay.matikan()
# jumlah = "2.500"
# harga = "500.000"
# lcd_display.display(jumlah, harga)

import waterpump
waterpump.setup_gpio()
waterpump.on()
waterpump.off()

# import contoh_waterpump

# contoh_waterpump.hidup()
# contoh_waterpump.mati()