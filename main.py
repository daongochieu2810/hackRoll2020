import cv2 as cv
import numpy as np

cars_cascade = cv.CascadeClassifier('./cars.xml')
video = './video.avi'
vid = cv.VideoCapture(video)
#bicycle_cascade = cv.CascadeClassifier('./bicycle.xml')
def on_trackbar(val):
    pass
cv.namedWindow("trackbar",cv.WINDOW_NORMAL)
cv.resizeWindow("trackbar",600,600)
cv.createTrackbar("scaleFactor","trackbar",11,50,on_trackbar)
cv.createTrackbar("minNeighbors","trackbar",1,20,on_trackbar)

def detect_cars(img,scale_factor,min_neighbors): 
      
    cars_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    cars_rect = cars_cascade.detectMultiScale(cars_img,scaleFactor=scale_factor,minNeighbors=min_neighbors) 
    print("Number of cars detected: %d" % len(cars_rect))
    for (x, y, w, h) in cars_rect: 
        cv.rectangle(img, (x, y),  
                      (x + w, y + h), (0, 255, 0), 2) 
          
    return img 

def processing(vid):
    
    scale_factor = 1.1
    min_neighbors = 1
    while True:
        _,img = vid.read()
        #img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        scale_factor = cv.getTrackbarPos("scaleFactor","trackbar")
        scale_factor = (float)(scale_factor/10.0)
        min_neighbors = cv.getTrackbarPos("minNeighbors","trackbar")
        cv.imshow("trackbar",detect_cars(img,scale_factor,min_neighbors))
        cv.waitKey(33)
        
processing(vid)

