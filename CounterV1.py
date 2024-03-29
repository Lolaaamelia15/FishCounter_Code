# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
import pandas as pd
from threading import Thread
import importlib.util
import math
from centroidtracker import CentroidTracker
from numpy import *

# Define and parse input arguments
parser = argparse.ArgumentParser()

parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    default='model')
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.80)
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='640x640')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')
parser.add_argument('--video', help='Name of the video file',
                    default='video.mp4')

args = parser.parse_args()

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
objects ={}
old_objects={}
dirlabels={}

# compare the co-ordinates for dictionaries of interest
def DictDiff(dict1, dict2):
   dict3 = {**dict1}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = np.subtract(dict2[key], dict1[key])
   return dict3

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu
VIDEO_NAME = args.video

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

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'       

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
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

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Open video file
VIDEO_PATH = os.path.join(CWD_PATH,VIDEO_NAME)
video = cv2.VideoCapture(VIDEO_PATH)
imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,640))

obsFrames = 0

jumlahIkanLewat = []

# Dictionary untuk melacak pergerakan objek
object_movements = {}

while(video.isOpened()): # Uncomment block for recorded video input
    # Acquire frame and resize to expected shape [1xHxWx3]
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()
    # On the next loop set the value of these objects as old for comparison
    old_objects.update(objects)
    ret, frame1 = video.read()
    if not ret:
      print('Reached the end of the video!')
      break
    # Acquire frame and resize to expected shape [1xHxWx3]
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[1]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects

    #rects variable
    rects =[]

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
            
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            if object_name == 'lele':
            
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                box = np.array([xmin,ymin,xmax,ymax])

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 4)
            
                rects.append(box.astype("int"))

                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
    
    #update the centroid for the objects
    objects = ct.update(rects)
    objectslist= pd.DataFrame.from_dict(objects).transpose()
    objectslist.columns = ['c','d']
    objectslist['index'] = objectslist.index
    
    for index, row in objectslist.iterrows():
        text = "ID {}".format(row['index'])
        cv2.putText(frame, text, (row['c'] - 10, row['d'] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    print(*objects, sep=",")
    print("Jumlah bibit : {}".format(len(objects)))
    
    if(len(objects) >= 3):
        break

    # Menampilkan jumlah bibit pada frame
    cv2.putText(frame, f'Jumlah Bibit: {len(objects)}', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

    # calculate the difference between this and the previous frame
    x = DictDiff(objects,old_objects)
    difflist= pd.DataFrame.from_dict(x).transpose()
    difflist.columns = ['a','b']
    difflist['index'] = difflist.index
    z = difflist.merge(objectslist,left_on = 'index', right_on = 'index', suffixes=('_diff','_current'))

    dirx = z['c']
    diry = z['d']

    for i,j,k in zip(dirlabels,dirx,diry):
        direction = format(dirlabels[i])
        cv2.putText(frame, direction, (j+ 10, k + 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 60, 255), 2)       

    # prints the direction of travel (if any) and timestamp
    print(dirlabels)
    
    # Draw framerate in corner of frame
    cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2,cv2.LINE_AA)

    vidout = cv2.resize(frame,(640,640))
    out.write(vidout)

    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1
    #count number of frames for direction calculation
    obsFrames = obsFrames + 1
    
    # Press 'q' to quit and give the total tally
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
video.release() #for recorded video
out.release() 
#videostream.stop() #for videostream