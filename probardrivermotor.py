from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels =16)
nbPCAServo=8 
#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
for i in range(nbPCAServo):
    kit.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
kit.servo[8].angle = 180
# for j in range(0, 0, 1):
#     kit.servo[8].angle = j
#     time.sleep(0.015)
#kit.servo[8].angle=None #disable channel
