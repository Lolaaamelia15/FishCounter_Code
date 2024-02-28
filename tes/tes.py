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
# # lcd_display.display(jumlah, harga)

# import waterpump
# waterpump.setup_gpio()
# waterpump.on()
# waterpump.off()

# # import contoh_waterpump

# # contoh_waterpump.hidup()
# # contoh_waterpump.mati()

# import buzzer

# buzzer.hidup()
# import Counter
# Counter.count(40)

import cv2
import numpy as np
import os
import time
import argparse
from centroidtracker import CentroidTracker

# Inisialisasi centroid tracker dan dimensi frame
ct = CentroidTracker(maxDisappeared=20)
objects = {}
old_objects = {}

# Fungsi untuk membandingkan koordinat antara dua dictionary
def DictDiff(dict1, dict2):
    dict3 = {**dict1}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = np.subtract(dict2[key], dict1[key])
    return dict3

# Mendefinisikan dan parsing argumen input
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder tempat file .tflite berada', default='model')
parser.add_argument('--graph', help='Nama file .tflite, jika berbeda dengan detect.tflite', default='detect.tflite')
parser.add_argument('--labels', help='Nama file labelmap, jika berbeda dengan labelmap.txt', default='labelmap.txt')
parser.add_argument('--threshold', help='Ambang batas kepercayaan minimum untuk menampilkan objek yang terdeteksi', default=0.80)
args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)

# Membaca label map
CWD_PATH = os.getcwd()
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Membaca model TensorFlow Lite
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)
interpreter = cv2.dnn.readNetFromTensorflow(PATH_TO_CKPT)

# Inisialisasi frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Mengatur resolusi webcam
imW, imH = 640, 480

# Mengaktifkan webcam
video = cv2.VideoCapture(0)

# Mengambil gambar dari webcam saat tombol ditekan
while True:
    ret, frame = video.read()
    cv2.imshow('Press SPACE to capture', frame)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        captured_frame = frame.copy()
        break

# Resize gambar yang ditangkap ke dimensi yang diharapkan
frame_resized = cv2.resize(captured_frame, (300, 300))

# Mengubah format gambar ke format yang diterima oleh model (blob)
input_data = cv2.dnn.blobFromImage(frame_resized, size=(300, 300), swapRB=True)

# Menyimpan gambar yang ditangkap
cv2.imwrite('captured_image.jpg', captured_frame)

# Performa deteksi objek menggunakan model TFLite
interpreter.setInput(input_data)
detections = interpreter.forward()

# Loop over semua deteksi dan gambar kotak deteksi jika kepercayaan di atas ambang batas minimum
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > min_conf_threshold:
        class_id = int(detections[0, 0, i, 1])
        if labels[class_id] == 'lele':  # Hanya menampilkan jika objek adalah bibit ikan
            box = detections[0, 0, i, 3:7] * np.array([imW, imH, imW, imH])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(captured_frame, (startX, startY), (endX, endY), (10, 255, 0), 4)
            label = '{}: {:.2f}%'.format(labels[class_id], confidence * 100)
            cv2.putText(captured_frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Menampilkan hasil deteksi
cv2.imshow('Detected Objects', captured_frame)
cv2.waitKey(0)

# Membersihkan
cv2.destroyAllWindows()
video.release()
