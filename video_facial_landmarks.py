from imutils.video import VideoStream
from imutils import face_utils
from playsound import playsound
import datetime
import argparse
import imutils
import time
import os
import dlib
import cv2
#from scipy.spatial import distance as dist
import numpy as np
from adafruit_servokit import ServoKit
nbPCAServo=6 
#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180]

def ojos_angulos(ojoder, ojoizq):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
        angulo_rad=np.arctan((ojoder[1]-ojoizq[1])/(ojoder[0]-ojoizq[0]))
        angulo_deg = np.degrees(angulo_rad)
        return angulo_deg

def mover_ojos(x_ant,x):
    if(x>x_ant):
        for j in range(x_ant, x, 1):
            #print("Send angle {}".format(j))
            pca.servo[2].angle = j*0.3 #Antes 0.45
            pca.servo[3].angle = j*0.3
            pca.servo[8].angle = j*0.3
            time.sleep(0.015)
        pca.servo[2].angle=None #disable channel
        pca.servo[3].angle=None #disable channel
        pca.servo[8].angle=None #disable channel
    else:
        for j in range(x_ant, x,-1):
           #print("Send angle {}".format(j))
           pca.servo[2].angle = j*0.3
           pca.servo[3].angle = j*0.3
           pca.servo[8].angle = j*0.3
           time.sleep(0.015)
        pca.servo[2].angle=None #disable channel
        pca.servo[3].angle=None #disable channel
        pca.servo[8].angle=None #disable channel
    return True

def mover_servo(angulo, angulo_anterior):
    if(angulo>angulo_anterior):
        for j in range(angulo_anterior, angulo,1):
            #print("Send angle {}".format(j))
            pca.servo[0].angle = j
            pca.servo[1].angle = j
            time.sleep(0.025)
        pca.servo[0].angle=None #disable channel
        pca.servo[1].angle=None #disable channel
    else:
        for j in range(angulo_anterior, angulo,-1):
            #print("Send angle {}".format(j))
            pca.servo[0].angle = j
            pca.servo[1].angle = j
            time.sleep(0.025)
        pca.servo[0].angle=None #disable channel
        pca.servo[1].angle=None #disable channel
    return True

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	# return the eye aspect ratio
	return ear

def mouth_ratio(mouth):
	# eye landmark (x, y)-coordinates
        C = dist.euclidean(mouth[0], mouth[6])
        S = dist.euclidean(mouth[14], mouth[18])
        return C, S
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-l", "--laugh", required=True,
	help="path to laughingman")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

#Objects
pca = ServoKit(channels=16)
for i in range(nbPCAServo):
    pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
pca.servo[0].angle = 90
pca.servo[1].angle = 90
pca.servo[2].angle = 90
pca.servo[3].angle = 90
pca.servo[4].angle = 0
pca.servo[5].angle = 45
ang_ant = 0
posx_ant = 200
primera_vuelta = True
for j in range(0, 45,1):
    pca.servo[4].angle = j
    pca.servo[5].angle = 45-j
    time.sleep(0.025)
pca.servo[4].angle=None #disable channel
pca.servo[5].angle=None #disable channel
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		ojoder_ext = shape[36]
		ojoder_cent = shape[39]
		ojoizq_ext = shape[45]
		ojoizq_cent = shape[42]
		nariz = shape[29]
		ang = round(ojos_angulos(ojoder_ext, ojoizq_ext))+90
		posx = nariz[0]
		posy = nariz[1]
		if(abs(posx-posx_ant)>5) and (primera_vuelta==False):
			[b, posx_ant] = [mover_ojos(posx_ant, posx), posx]
		elif (primera_vuelta==True):
			[posx_ant, primera_vuelta] = [posx, False]
		
		if (abs(ang-ang_ant)>3):
			[a, ang_ant] = [mover_servo(ang, ang_ant), ang]
		
		ojo_der = shape[42:48]
		ojo_izq = shape[36:42]
		boca = shape[48:68]
		distanciaComisura = abs(boca[0][0]-boca[6][0])
		distanciaSonrisa = abs(boca[14][1]-boca[18][1])
		print(distanciaComisura)
		if (distanciaSonrisa>8 and distanciaComisura>42):
			print("SONRISA")
			playsound(args["laugh"])
            
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
	  
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


#python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1