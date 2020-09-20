from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2 as cv
from Servo import Servo

faceCascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

yawServo = Servo(17)

#PID Controller setup
P, I, D = 0.1, 0, 0
integral = 0
differential = 0
previousError = 0

#Camera setup
width, height = 320, 240
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = (width, height))
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    image = frame.array
    frame = cv.flip(image, 0)
    #frame = cv.flip(frame, 0)

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #convert to greyscale

    faces = faceCascade.detectMultiScale(grayFrame, 1.3, 5) #Find all faces in frame using haar cascade

    for(x,y,w,h) in faces:
        faceCentroidX = x + w / 2
        error = width / 2 - faceCentroidX #use distance of face from center of frame as error
        integral += error
        differential = previousError - error
        previousError = error

        adjustmentValue = P * error + I * integral + D * differential
        yawServo.changeAngle(-adjustmentValue)

        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4) #highlight face with rectangle
        
        break #only consider the first face
    
    cv.imshow('ComputerView',frame) #display image
    key = cv.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
 
cv2.destroyAllWindows()
