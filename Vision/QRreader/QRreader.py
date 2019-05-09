from picamera.array import PiRGBArray
from picamera import PiCamera
from pyzbar import pyzbar

import imutils
import cv2
import time

resY = 640 #800
resX = 480 #608

camera = PiCamera()
camera.resolution = (resY, resX)

rawCapture = PiRGBArray(camera, size=(resY, resX))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    rawCapture.truncate()
    rawCapture.seek(0)
    
    img = frame.array
    
    rawCapture.truncate(0)
    
    start = time.time()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 60, 225, cv2.THRESH_BINARY)[1]
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            
            if ar >= 0.95 and ar <= 1.05 and w > 2:
                print("rect found")
                qrcodes = pyzbar.decode(gray)

                for qrcode in qrcodes:
                    data = qrcode.data.decode("utf-8")
                    if(len(data) > 0):
                        print("Decoded data: ", data)
    
    print("time: ", time.time() - start)
   
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()