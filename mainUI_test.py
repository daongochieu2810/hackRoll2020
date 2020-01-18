import cv2 as cv
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import atexit
import os
import sys
import webbrowser
import time
import numpy as np

#Optic Flow params

feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
color = np.random.randint(0,255,(100,3))


#################
backsub = cv.createBackgroundSubtractorMOG2()

classifierFile = "./cars.xml"

video0 = cv.VideoCapture("./cars1.avi")
video1 = cv.VideoCapture("./cars2.avi")
video2 = cv.VideoCapture("./road.avi")
video3 = cv.VideoCapture("./pedestrians.avi")
video4 = cv.VideoCapture("./road2.avi")
video5 = cv.VideoCapture("./pedestrians2.avi")

video = video0
allVideos = [video0, video1, video2, video3, video4,video5]

scale_factor = 1.1
min_neighbors = 2
i = 0
numberDetected = 0


def writeFile(numberDetected):
    global f
    f.write("%d," % (numberDetected))


def changeCCTV():
    global f, i
    global video
    #lines = f.readlines()
    video = allVideos[(i+1) % len(allVideos)]
    f.write("\n")
    i += 1


def finish_handler():
    global f,num_frame,end
    end = time.time()
    fps = num_frame/(end-start)
    print("Frame Rate: %.02f" % fps)
    f.close()
    os.system(
        '/usr/bin/python3  heatMap.py')

    os.system(
        '/usr/bin/python3  barGraph.py')
    webbrowser.open('./index.html')
    sys.exit()
    


def finish():
    finish_handler()


def exit():
    global num_frame,end,start
    end = time.time()
    fps = num_frame/(end-start)
    print("Frame rate: %.02f" %fps)
    sys.exit()


def changeToMotor():
    global classifierFile, scale_factor, min_neighbors
    classifierFile = "./bikes.xml"
    scale_factor = 1.4
    min_neighbors = 1


def changeToCars():
    global classifierFile, scale_factor, min_neighbors
    classifierFile = "./cars.xml"
    scale_factor = 1.1
    min_neighbors = 2


def changeToPedestrian():
    global classifierFile, scale_factor, min_neighbors
    classifierFile = "./pedestrian.xml"
    scale_factor = 1.3
    min_neighbors = 2


def processed(frame, scale_factor, min_neighbors):
    global classifierFile
    img = frame
    #fgbg = cv.createBackgroundSubtractorMOG2()
    #img = fgbg.apply(img)
    # cv.imshow("test",fgbg)
    # cv.waitKey(33)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    classifier = cv.CascadeClassifier(classifierFile)
    objects = classifier.detectMultiScale(
        img, scaleFactor=scale_factor, minNeighbors=min_neighbors)
    writeFile(len(objects))
    for x, y, w, h in objects:
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    return frame


window = Tk()
window.geometry("1200x500")
window.title("Main Window")

# bkPhoto = Image.open('./image.jpeg')
# bkPhoto = ImageTk.PhotoImage(bkPhoto.resize((1200, 500), Image.ANTIALIAS))
# b = Label(window, text="Finish", width=10)
# b.config(image=bkPhoto)
# b.grid(row=0, column=0, sticky=W)

#background_image= ImageTk.PhotoImage(Image.open('./background.png'))
#background_label = tk.Label(window, image=background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)


#window.style = Style()
# window.style.theme_use("classic")

panel1 = Label(window)
panel1.grid(row=0, column=0, padx=10, pady=10)

panel2 = Label(window)
panel2.grid(row=0, column=2, padx=10, pady=10)

#bikePhoto = Image.open('./button.png')
#bikePhoto = ImageTk.PhotoImage(bikePhoto.resize((150, 50), Image.ANTIALIAS))

bikeButton = Button(window, text="Bikes", width=10, command=changeToMotor)
# bikeButton.config(image=bikePhoto)
bikeButton.grid(row=0, column=1, sticky=W, padx=20, pady=20)
bikeButton.place(relx=.8, rely=.08, anchor="c")

pdtButton = Button(window, text="Pedestrians",
                   width=10, command=changeToPedestrian)
pdtButton.grid(row=1, column=1, sticky=W, padx=20, pady=20)
pdtButton.place(relx=.8, rely=.2, anchor="c")


carsButton = Button(window, text="Cars", width=10, command=changeToCars)
carsButton.grid(row=2, column=1, sticky=W, padx=20, pady=20)
carsButton.place(relx=.8, rely=.3, anchor="c")

f = open(f"data.csv", 'w')
changeCCTVButton = Button(window, text="change CCTV",
                          width=20, command=changeCCTV)
changeCCTVButton.grid(row=1, column=1, sticky=W, padx=20, pady=20)
changeCCTVButton.place(relx=.8, rely=.5, anchor="c")


#finishPhoto = Image.open('./finishButton.png')
#finishPhoto = ImageTk.PhotoImage(finishPhoto.resize((150, 50), Image.ANTIALIAS))
finishButton = Button(window, text="Finish",
                      width=10, command=finish)
# finishButton.config(image=finishPhoto)
finishButton.grid(row=1, column=2, sticky=W, padx=20, pady=20)
finishButton.place(relx=.8, rely=.6, anchor="c")

exitButton = Button(window, text="Exit",
                    width=10, command=exit)
# finishButton.config(image=finishPhoto)
exitButton.grid(row=1, column=2, sticky=W, padx=20, pady=20)
exitButton.place(relx=.8, rely=.7, anchor="c")


def bgSubtract(img):
    global backsub
    bgMask = backsub.apply(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
    cv.rectangle(img, (10, 2), (100, 20), (255, 255, 255), -1)

    return bgMask

num_frame = 0
def video_stream(scale_factor, min_neighbors):
    global i,num_frame,old_gray,p0

    ret, frame = video.read()
    num_frame+=1
    mask = frame.copy()
    if not ret:
        video.set(1, 0)
        video_stream(scale_factor, min_neighbors)
    im_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    if num_frame==1:
        old_gray = im_gray.copy()
        p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    else:
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, im_gray, p0, None, **lk_params)
        good_new = p1[st==1]
        good_old = p0[st==1]
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new, good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            mask = cv.line(mask, (a,b),(c,d), color[i].tolist(), 1)
            frame = cv.circle(frame,(a,b),5,color[i].tolist(),-1)
        img = cv.add(frame,mask)
        cv.imshow('frame',img)
        cv.waitKey(1)
    # Now update the previous frame and previous points
        old_gray = im_gray.copy()
        p0 = good_new.reshape(-1,1,2)
    

    bgST = bgSubtract(frame)
    img = cv.cvtColor(processed(frame, scale_factor,
                                min_neighbors), cv.COLOR_BGR2RGBA)

    img = Image.fromarray(img)
    img = img.resize((400, 400), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)

    bgST = Image.fromarray(bgST)
    bgST = bgST.resize((400, 400), Image.ANTIALIAS)
    imgtk2 = ImageTk.PhotoImage(image=bgST)

    panel2.imgtk = imgtk2
    panel2.configure(image=imgtk2)

    panel1.imgtk = imgtk
    panel1.configure(image=imgtk)
    panel1.after(1, lambda: video_stream(scale_factor, min_neighbors))


video_stream(scale_factor, min_neighbors)
start = time.time()
window.mainloop()
end = time.time()
fps = num_frame/(end-start)
print("Frame Rate: %d" % fps)
video.release()
