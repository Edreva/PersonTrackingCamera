import RPi.GPIO as GPIO          
from time import sleep

#Servo specific values
upperDC = 12
lowerDC = 2
rangeDC = upperDC - lowerDC
maxAngle = 180

class Servo():
    def __init__(self, servoPin):   #setup
        GPIO.setmode(GPIO.BCM) #notice BCM pin labels
        GPIO.setwarnings(False)
        GPIO.setup(servoPin,GPIO.OUT)
        
        self.servoPWM = GPIO.PWM(servoPin, 50)
        self.servoPWM.start(rangeDC / 2 + lowerDC)
        self.currentAngle = maxAngle / 2
        sleep(1)
        self.servoPWM.ChangeDutyCycle(0)
        
    def __del__(self): #destructor
        self.servoPWM.stop()
        GPIO.cleanup()
        
    def setDC(self, dc): #Safely sets the duty cycle
        self.servoPWM.ChangeDutyCycle(dc)
        sleep(0.05)
        self.servoPWM.ChangeDutyCycle(0)
        self.currentAngle = (dc - lowerDC) / rangeDC * maxAngle

    def setAngle(self, angle): #Calculate angles corresponding duty cycle
        if(angle <= 0):
            angle = 1
        if(angle >= maxAngle):
            angle = maxAngle
        self.servoPWM.ChangeDutyCycle(angle / maxAngle * rangeDC + lowerDC)
        sleep(0.05)
        self.servoPWM.ChangeDutyCycle(0)
        self.currentAngle = angle

    def changeAngle(self, delta): #increments/decrements angle of servo
        self.currentAngle += delta
        self.setAngle(self.currentAngle)