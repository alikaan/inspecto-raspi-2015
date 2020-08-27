import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BOARD)
pin = 7
GPIO.setup(pin, GPIO.OUT)
 
pwm = GPIO.PWM(pin, 50)
pwm.start(0)
 
try:
    while True:     
        for i in range(100):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.02)
        for i in range(100):
            pwm.ChangeDutyCycle(100-i)
            time.sleep(0.02)
except KeyboardInterrupt:
    pass

pwm.stop() 
GPIO.cleanup()
