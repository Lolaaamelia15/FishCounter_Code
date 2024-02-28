# import RPi.GPIO as GPIO
# import os
# import time
# import cv2
# import numpy as np
# import sys
# import pandas as pd

# from centroidtracker import CentroidTracker

# # Define GPIO pin for push button
# BUTTON_PIN = 18

# # Set up GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # Initialize Centroid Tracker
# ct = CentroidTracker(maxDisappeared=5)
# jumlahIkan = []

# # Define and load the TFLite model
# MODEL_NAME = 'model'
# GRAPH_NAME = 'detect.tflite'
# LABELMAP_NAME = 'labelmap.txt'

# PATH_TO_CKPT = os.path.join(MODEL_NAME, GRAPH_NAME)
# PATH_TO_LABELS = os.path.join(MODEL_NAME, LABELMAP_NAME)

# interpreter = cv2.dnn_DetectionModel(PATH_TO_CKPT, PATH_TO_LABELS)
# interpreter.setInputSize(300, 300)
# interpreter.setInputScale(1.0 / 127.5)
# interpreter.setInputMean((127.5, 127.5, 127.5))
# interpreter.setInputSwapRB(True)

# # Function to handle button press
# def button_pressed(channel):
#     print("Button pressed!")
#     cap = cv2.VideoCapture(0)  # Access the webcam (change to appropriate index if multiple cameras)

#     ret, frame = cap.read()  # Capture frame-by-frame

#     # Save captured frame as an image
#     cv2.imwrite('captured_image.jpg', frame)

#     # Release the capture
#     cap.release()

#     # Perform object detection on the captured image
#     detect_objects('captured_image.jpg')

# def detect_objects(image_path):
#     # Load the captured image
#     frame = cv2.imread(image_path)

#     # Detect objects
#     classes, scores, boxes = interpreter.detect(frame, confThreshold=0.85)

#     if boxes is not None:
#         rects = []
#         for classId, score, box in zip(classes.flatten(), scores.flatten(), boxes):
#             if classId == 1:  # Check if the detected object is a fish
#                 cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
#                 rects.append(box.astype("int"))
        
#         # Update centroid tracker with detected rectangles
#         objects = ct.update(rects)

#         # Display ID of each object
#         for obj_id, centroid in objects.items():
#             cv2.putText(frame, f'ID {obj_id}', (centroid[0] - 10, centroid[1] - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # Display total number of detected objects
#         cv2.putText(frame, f'Jumlah Bibit: {len(objects)}', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),
#                     2)

#         # Show the frame
#         cv2.imshow('Detected Objects', frame)
#         cv2.waitKey(0)

# # Add event listener for button press
# GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

# try:
#     while True:
#         time.sleep(1)  # Keep the main program running

# except KeyboardInterrupt:
#     print("Cleaning up GPIO...")
#     GPIO.cleanup()



# Versi kedua : akan mengambil gambar baru setiap kali tombol ditekan

# import RPi.GPIO as GPIO
# import time
# import cv2
# import numpy as np
# import sys
# import pandas as pd
# from centroidtracker import CentroidTracker

# # Define GPIO pin for push button
# BUTTON_PIN = 18

# # Set up GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # Initialize Centroid Tracker
# ct = CentroidTracker(maxDisappeared=5)
# jumlahIkan = []

# # Define and load the TFLite model
# MODEL_NAME = 'model'
# GRAPH_NAME = 'detect.tflite'
# LABELMAP_NAME = 'labelmap.txt'

# PATH_TO_CKPT = os.path.join(MODEL_NAME, GRAPH_NAME)
# PATH_TO_LABELS = os.path.join(MODEL_NAME, LABELMAP_NAME)

# interpreter = cv2.dnn_DetectionModel(PATH_TO_CKPT, PATH_TO_LABELS)
# interpreter.setInputSize(300, 300)
# interpreter.setInputScale(1.0 / 127.5)
# interpreter.setInputMean((127.5, 127.5, 127.5))
# interpreter.setInputSwapRB(True)

# # Function to handle button press
# def button_pressed(channel):
#     print("Button pressed!")
#     cap = cv2.VideoCapture(0)  # Access the webcam (change to appropriate index if multiple cameras)

#     ret, frame = cap.read()  # Capture frame-by-frame

#     # Save captured frame as an image
#     cv2.imwrite('captured_image.jpg', frame)

#     # Release the capture
#     cap.release()

#     # Perform object detection on the captured image
#     detect_objects('captured_image.jpg')

#     # Sleep to avoid multiple button presses
#     time.sleep(1)

# def detect_objects(image_path):
#     # Load the captured image
#     frame = cv2.imread(image_path)

#     # Detect objects
#     classes, scores, boxes = interpreter.detect(frame, confThreshold=0.85)

#     if boxes is not None:
#         rects = []
#         for classId, score, box in zip(classes.flatten(), scores.flatten(), boxes):
#             if classId == 1:  # Check if the detected object is a fish
#                 cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
#                 rects.append(box.astype("int"))
        
#         # Update centroid tracker with detected rectangles
#         objects = ct.update(rects)

#         # Display ID of each object
#         for obj_id, centroid in objects.items():
#             cv2.putText(frame, f'ID {obj_id}', (centroid[0] - 10, centroid[1] - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # Display total number of detected objects
#         cv2.putText(frame, f'Jumlah Bibit: {len(objects)}', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),
#                     2)

#         # Show the frame
#         cv2.imshow('Detected Objects', frame)
#         cv2.waitKey(0)

# # Add event listener for button press
# GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

# try:
#     while True:
#         time.sleep(1)  # Keep the main program running

# except KeyboardInterrupt:
#     print("Cleaning up GPIO...")
#     GPIO.cleanup()

# versi ketiga
import os
import sys
import argparse
import cv2
import numpy as np
import pandas as pd
import keyboard
import time
import importlib.util
from centroidtracker import CentroidTracker

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    default='model')
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.85)
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()


# Initialize Centroid Tracker
ct = CentroidTracker(maxDisappeared=30)
objects ={}
old_objects={}
dirlabels={}
jumlahIkan = []
jumlahIkan = []

# Parse user inputs
MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels

min_conf_threshold = float(args.threshold)
use_TPU = args.edgetpu

# # Define and load the TFLite model
# MODEL_NAME = 'model'
# GRAPH_NAME = 'detect.tflite'
# LABELMAP_NAME = 'labelmap.txt'

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Check output layer name to determine if this model was created with TF2 or TF1,
# because outputs are ordered differently for TF2 and TF1 models
outname = output_details[0]['name']

if ('StatefulPartitionedCall' in outname): # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else: # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2

# Function to handle spacebar press
def spacebar_pressed(e):
    if e.name == 'space':
        print("Spacebar pressed!")
        cap = cv2.VideoCapture(0)  # Access the webcam (change to appropriate index if multiple cameras)

        ret, frame = cap.read()  # Capture frame-by-frame

        # Save captured frame as an image
        cv2.imwrite('captured_image.jpg', frame)

        # Release the capture
        cap.release()

        # Perform object detection on the captured image
        detect_objects('captured_image.jpg')

        # Sleep to avoid multiple spacebar presses
        time.sleep(2)

def detect_objects(image_path):
    # Load the captured image
    frame = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imH, imW, _ = frame.shape 
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

 # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

    rects = []

    # Loop over all rects and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            object_name = labels[int(classes[i])]
            if object_name == 'lele':

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                box = np.array([xmin,ymin,xmax,ymax])
                
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                rects.append(box.astype("int"))
                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

                # rects.append([object_name, scores[i], xmin, ymin, xmax, ymax])
                

            if len(rects) > 0:
                objects = ct.update(rects)
                objectslist = pd.DataFrame.from_dict(objects).transpose()
                objectslist.columns = ['c', 'd']
                objectslist['index'] = objectslist.index

                for index, row in objectslist.iterrows():
                    if row['index'] not in jumlahIkan:
                        jumlahIkan.append(row['index'])

                    # Menampilkan ID masing-masing object
                    text = "ID {}".format(row['index'])
                    cv2.putText(frame, text, (row['c'] - 10, row['d'] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            print(*jumlahIkan, sep=",")
            print("Jumlah Ikan : {}".format(len(jumlahIkan))) 

            # Menampilkan jumlah ID pada frame 
            cv2.putText(frame, f'Jumlah Bibit: {len(jumlahIkan)}', (30,90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Show the frame
        cv2.imshow('Detected Objects', frame)
        cv2.waitKey(0)

# Add event listener for spacebar press
keyboard.on_press(spacebar_pressed)

try:
    while True:
        time.sleep(2)  # Keep the main program running

except KeyboardInterrupt:
    print("Cleaning up...")
    cv2.destroyAllWindows()

