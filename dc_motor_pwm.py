import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
motor_in1 = 16
motor_in2 = 18
motor_pwm = 22

GPIO.setup(motor_in1,GPIO.OUT)
GPIO.setup(motor_in2,GPIO.OUT)
GPIO.setup(motor_pwm,GPIO.OUT)

pwm  = GPIO.PWM(motor_pwm,50)
pwm.start(0)
pwm.ChangeDutyCycle(0)

GPIO.output(motor_in1,GPIO.HIGH)
GPIO.output(motor_in2,GPIO.LOW)

try:
    while True:     
        for i in range(100):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.2)
        for i in range(100):
            pwm.ChangeDutyCycle(100-i)
            time.sleep(0.2)
except KeyboardInterrupt:
    pass
    
GPIO.output(motor_in1,GPIO.LOW)
GPIO.output(motor_in2,GPIO.LOW)
pwm.stop()

GPIO.cleanup()
