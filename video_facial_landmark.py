from imutils.video import VideoStream
from imutils import face_utils
#from playsound import playsound
import argparse
import imutils
import time
import os
import dlib
import cv2
from pygame import mixer
#from scipy.spatial import distance as dist
import numpy as np
from adafruit_servokit import ServoKit
nbPCAServo=8 
#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180, 180, 180]

def ojos_angulos(ojoder, ojoizq):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
        angulo_rad=np.arctan((ojoder[1]-ojoizq[1])/(ojoder[0]-ojoizq[0]))
        angulo_deg = np.degrees(angulo_rad)
        return angulo_deg

def mover_ojos(x_ant,x):
    #print(x)
    if(x>x_ant):
        for j in range(x_ant, x, 1):
            #print("Send angle {}".format(j))
            pca.servo[2].angle = j*0.41 #Antes 0.45
            pca.servo[3].angle = j*0.41
            pca.servo[8].angle = j*0.45
            time.sleep(0.015)
        pca.servo[2].angle=None #disable channel
        pca.servo[3].angle=None #disable channel
        pca.servo[8].angle=None #disable channel
    else:
        for j in range(x_ant, x,-1):
           #print("Send angle {}".format(j))
           pca.servo[2].angle = j*0.41
           pca.servo[3].angle = j*0.41
           pca.servo[8].angle = j*0.45
           time.sleep(0.015)
        pca.servo[2].angle=None #disable channel
        pca.servo[3].angle=None #disable channel
        pca.servo[8].angle=None #disable channel
    return True

# def mover_ojosy(y_ant,y):
#     #print(x)
#     if(y>y_ant):
#         for j in range(y_ant, y, 1):
#             #print("Send angle {}".format(j))
#             pca.servo[0].angle = 90+j*0.36 #Antes 0.45
#             pca.servo[1].angle = 90-j*0.36
#             time.sleep(0.025)
#         pca.servo[0].angle=None #disable channel
#         pca.servo[1].angle=None #disable channel
#     else:
#         for j in range(y_ant, y,-1):
#            #print("Send angle {}".format(j))
#            pca.servo[0].angle = 90-j*0.36
#            pca.servo[1].angle = 90+j*0.36
#            time.sleep(0.025)
#         pca.servo[0].angle=None #disable channel
#         pca.servo[1].angle=None #disable channel
#     return True

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
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-l", "--laugh", required=True,
	help="path to laughingman")
#ap.add_argument("-t", "--triste", required=True,
#	help="path to laughingman")
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
pca.servo[8].angle = 90
ang_ant = 0
posx_ant = 200
posy_ant = 200
primera_vuelta = True
for j in range(0, 45,1):
    pca.servo[4].angle = j
    pca.servo[5].angle = 45-j
    time.sleep(0.025)
pca.servo[4].angle=None #disable channel
pca.servo[5].angle=None #disable channel
rectcount = 0
rectcount_ant = 0
mixer.init()
sound = mixer.Sound(args["laugh"])
triste = mixer.Sound('cries-female3.wav')
shall = mixer.Sound('shall-we.wav')
shall.play()
time.sleep(1)
inclinado = False
Frametriste=0
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
    rectcount = len(rects)
    #print("Cantidad caras actual: ", rectcount)
    #print("Cantidad caras anterior: ", rectcount_ant)
    if (rectcount > rectcount_ant) and (rectcount!= 1):
        print("Posando en cara", rectcount-1)
        shape = predictor(gray, rects[rectcount-1])
        shape = face_utils.shape_to_np(shape)
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
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
            mover_ojos(posx_ant, posx)
            posx_ant = posx
        if (primera_vuelta==True):
            [posx_ant, primera_vuelta] = [posx, False]
            #posy_ant = posy
        #if(abs(posy-posy_ant)>5 and primera_vuelta == False):
            #mover_ojosy(posy_ant, posy)
            #posy_ant = posy
        #if(abs(ang-ang_ant)>3):
         #   [a, ang_ant] = [mover_servo(ang, ang_ant), ang        
    elif(rectcount != 0 or (rectcount == rectcount_ant and rectcount>1)):
        print("Posando en cara 0")
        shape = predictor(gray, rects[0])
        shape = face_utils.shape_to_np(shape)
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        # loop over the (x, y)-coordinates for the facial landmarks
    	# and draw them on the image
        ojoder_ext = shape[36]
        ojoder_cent = shape[39]
        ojoizq_ext = shape[45]
        ojoizq_cent = shape[42]
        factorconver = abs(ojoder_ext[0]-ojoizq_ext[0])/10 #10cm
        nariz = shape[29]
        ang = round(ojos_angulos(ojoder_ext, ojoizq_ext))+90
        posx = nariz[0]
        posy = nariz[1]
        if(abs(posx-posx_ant)>5) and (primera_vuelta==False):
            mover_ojos(posx_ant, posx)
            posx_ant = posx
        #if (abs(posy_ant-posy)>5) and (primera_vuelta==False):
        #    mover_ojosy(posy_ant, posy)
         #   posy_ant = posy
        if (primera_vuelta==True):
            [posx_ant, primera_vuelta] = [posx, False]
            #posy_ant = posy
        if (abs(ang-ang_ant)>3):
            mover_servo(ang, ang_ant)
            ang_ant = ang
            inclinado = True
        boca = shape[48:68]
        distanciaComisura = abs(boca[0][0]-boca[6][0])/factorconver
        distanciaSonrisa = abs(boca[14][1]-boca[18][1])/factorconver
        distanciaTriste = abs(boca[0][1]-boca[18][1])/factorconver
        print(distanciaTriste)
        if (distanciaSonrisa>1) and (distanciaComisura>7) and (mixer.get_busy()==False):
            #print("SONRISA")            
            for j in range(46, 0,2):
                pca.servo[4].angle = j
                pca.servo[5].angle = 46-j
                time.sleep(0.01)
            sound.play()
            time.sleep(2)
            for j in range(0, 45,1):
                pca.servo[4].angle = j
                pca.servo[5].angle = 45-j
                time.sleep(0.01)
            pca.servo[4].angle=None #disable channel
            pca.servo[5].angle=None #disable channel
        elif (inclinado == False) and (distanciaTriste>0.6) and (mixer.get_busy()== False):
            Frametriste = Frametriste + 1
            if (Frametriste > 3):
                for j in range(46, 0,2):
                    pca.servo[4].angle = j
                    pca.servo[5].angle = 46-j
                    time.sleep(0.01)
                triste.play()
                time.sleep(2.25)
                mixer.stop()
                Frametriste = 0
    rectcount_ant = rectcount
    inclinado = False  
	# show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
	# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()