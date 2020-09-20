import RPi.GPIO as GPIO          
from time import sleep

upperDC = 12
lowerDC = 2
rangeDC = upperDC - lowerDC
maxAngle = 180

class Servo():
    def __init__(self, servoPin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(servoPin,GPIO.OUT)
        self.servoPWM = GPIO.PWM(servoPin, 50)
        self.servoPWM.start(rangeDC / 2 + lowerDC)
        self.currentAngle = maxAngle / 2
        sleep(1)
        self.servoPWM.ChangeDutyCylce(0)
        
    def __del__(self):
        self.servoPWM.stop()
        GPIO.cleanup()
        
    def setDC(self, dc):
        self.servoPWM.ChangeDutyCycle(dc)
        sleep(0.05)
        self.servoPWM.ChangeDutyCycle(0)
        self.currentAngle = (dc - lowerDC) / rangeDC * maxAngle

    def setAngle(self, angle):
        self.servoPWM.ChangeDutyCycle(angle / maxAngle * rangeDC + lowerDC)
        sleep(0.05)
        self.servoPWM.ChangeDutyCycle(0)
        self.currentAngle = angle

    def changeAngle(self, delta):
        self.currentAngle += delta
        self.setAngle(self.currentAngle)
        
