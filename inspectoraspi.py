import RPi.GPIO as GPIO
from time import sleep
import cv2 
import numpy as np

pwm_value = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# motor 1 pins
motor_in1_m1 = 16
motor_in2_m1 = 18
motor_pwm_m1 = 22
# motor 2 pins
motor_in1_m2 = 13
motor_in2_m2 = 15
motor_pwm_m2 = 11
# motor 1 setup
GPIO.setup(motor_in1_m1,GPIO.OUT)
GPIO.setup(motor_in2_m1,GPIO.OUT)
GPIO.setup(motor_pwm_m1,GPIO.OUT)
# motor 2 setup
GPIO.setup(motor_in1_m2,GPIO.OUT)
GPIO.setup(motor_in2_m2,GPIO.OUT)
GPIO.setup(motor_pwm_m2,GPIO.OUT)
# motor 1 pwm
pwm_m1 = GPIO.PWM(motor_pwm_m1,19)
pwm_m1.start(0)
pwm_m1.ChangeDutyCycle(0)
#motor 2 pwm
pwm_m2 = GPIO.PWM(motor_pwm_m2,19)
pwm_m2.start(0)
pwm_m2.ChangeDutyCycle(0)
# motor 1
GPIO.output(motor_in1_m1,GPIO.LOW)
GPIO.output(motor_in2_m1,GPIO.LOW)
# motor 2
GPIO.output(motor_in1_m2,GPIO.LOW)
GPIO.output(motor_in2_m2,GPIO.LOW)


def forward():
    # motor 1
    GPIO.output(motor_in1_m1,GPIO.HIGH)
    GPIO.output(motor_in2_m1,GPIO.LOW)
    # motor 2
    GPIO.output(motor_in1_m2,GPIO.HIGH)
    GPIO.output(motor_in2_m2,GPIO.LOW)
	# set pwm
    pwm_m1.ChangeDutyCycle(pwm_value)
    pwm_m2.ChangeDutyCycle(pwm_value)
    print "forward"
def reverse():
    # motor 1
    GPIO.output(motor_in1_m1,GPIO.LOW)
    GPIO.output(motor_in2_m1,GPIO.HIGH)
    # motor 2
    GPIO.output(motor_in1_m2,GPIO.LOW)
    GPIO.output(motor_in2_m2,GPIO.HIGH)
    # set pwm
	pwm_m1.ChangeDutyCycle(pwm_value)
    pwm_m2.ChangeDutyCycle(pwm_value)
    print "reverse"
def stop():
    # motor 1
    GPIO.output(motor_in1_m1,GPIO.LOW)
    GPIO.output(motor_in2_m1,GPIO.LOW)
    # motor 2
    GPIO.output(motor_in1_m2,GPIO.LOW)
    GPIO.output(motor_in2_m2,GPIO.LOW)
    pwm_m1.ChangeDutyCycle(pwm_value)
    pwm_m2.ChangeDutyCycle(pwm_value)
    print "stop"
def motor1():
    GPIO.output(motor_in1_m1,GPIO.HIGH)
    GPIO.output(motor_in2_m1,GPIO.LOW)
    pwm_m1.ChangeDutyCycle(pwm_value)
    print "left"
def motor2():
    GPIO.output(motor_in1_m2,GPIO.HIGH)
    GPIO.output(motor_in2_m2,GPIO.LOW)
    pwm_m2.ChangeDutyCycle(pwm_value)
    print "right"

def depth(area):
    stop()
    if ( area < 600 ):
	forward()
    elif ( area > 2000 ):
	reverse()
    else:
	stop()

def tracing(x):
    stop()
    if ( x < 40 ):
	motor1()
    elif ( x > 120 ):
	motor2()
    else:
	stop()	

# opencv 
Hmin = 0
Hmax = 36

Smin = 119
Smax = 237

Vmin = 169
Vmax = 255

rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

minArea = 50

cv2.namedWindow("Frame")
cv2.namedWindow("HSV")
cv2.namedWindow("Thresh")
cv2.namedWindow("Dilate")
cv2.namedWindow("Erode")


capture = cv2.VideoCapture(0)

width = 160
height = 120

# opencv
if capture.isOpened():
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  
while True:
    ret, frame = capture.read()
    imgMedian = cv2.medianBlur(frame,1)
    imgHSV = cv2.cvtColor(imgMedian,cv2.COLOR_BGR2HSV)	
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgGaussianBlur = cv2.GaussianBlur(imgThresh, (3, 3), 2)
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgGaussianBlur, kern_dilate) #np.ones((5,5),np.uint8))
    imgErode = cv2.erode(imgDilate, kern_erode)#np.ones((5,5),np.uint8) ) #None, iterations = 3
    moments = cv2.moments(imgDilate, True)
    area = moments['m00']
    stop()
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(imgErode,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=0,maxRadius=0)
    # circles = np.uint16(np.around(circles))

    #Draw Circles
    if circles is not None:
            for i in circles[0,:]:
                # If the ball is far, draw it in 
		x, y, radius = i
   		cv2.circle(frame, (x, y), radius, (0, 0, 255), 3)
		
    if area >= minArea:
    	x = moments['m10'] / moments['m00']
        y = moments['m01'] / moments['m00']
        print(x, ", ", y, ",",area)
	cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
	depth(area)

    cv2.imshow("Frame",frame)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Thresh", imgThresh)
    cv2.imshow("Dilate", imgDilate)
    cv2.imshow("Erode", imgErode)

    if cv2.waitKey(10) == 27:
        break


cv2.destroyAllWindows()
pwm_m1.stop()
pwm_m2.stop()
GPIO.cleanup()
