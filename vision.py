'''imports'''
import time
import argparse
import logging
from threading import Thread
try: #things that could error go here
    import VisionMap
    import cv2
    import numpy
    from networktables import NetworkTable
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except ImportError:
    print("Could not import cv2/picamera/networktables. Have you ran\nsource~/.profile & workon cv?")
    raise

class PiVideoStream:
    def __init__(self):
        #initialize camera and stream
        self.camera = PiCamera()
        self.camera.resolution = VisionMap.resolution
        self.camera.framerate = VisionMap.framerate
        self.camera.shutter_speed = VisionMap.exposure
        self.camera.brightness = VisionMap.brightness
        self.camera.sharpness = VisionMap.sharpness
        self.camera.saturation = VisionMap.saturation
        self.camera.rotation = VisionMap.rotation
        self.rawCapture =  PiRGBArray(self.camera, size=VisionMap.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        time.sleep(2)
        
        #create frame and shouldRun variable
        self.image = None
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        #loop intill thread stops
        for frame in self.stream:
            self.image = frame.array
            #cv2.imshow("orig", self.image)
            #cv2.waitKey(1)            
            self.rawCapture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return self.image

    def stop(self):
        self.stopped = True

def nothing(x):
    pass

def processImage(origImage):
    #cv2.imshow("original", origImage)
    outImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2HSV)
    outImage = cv2.medianBlur(outImage, 3)
    #cv2.imshow("blur", outImage)
    outImage = cv2.inRange(outImage, VisionMap.hsvLower, VisionMap.hsvUpper)
    #cv2.imshow("HSV", outImage)
    outImage = cv2.Canny(outImage, VisionMap.cannyThreshMin, VisionMap.cannyThreshMax)
    #cv2.imshow("Canny", outImage)
    (outImage, contours, _) = cv2.findContours(outImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    outImage = cv2.drawContours(origImage, contours, -1, (255, 255, 0), 1)
    #cv2.imshow("final", outImage)
    contoursFinal = []
    for contour in contours:
        '''currentContour = cv2.drawContours(origImage, contour, -1, (255, 0, 255), 2)
        cv2.imshow("Current Contour", currentContour)
        cv2.waitKey(1)
        print(i)'''

        '''area'''
        area = cv2.contourArea(contour)
        if area > VisionMap.areaMin and area < VisionMap.areaMax:
            
            '''perimeter'''
            perimeter = cv2.arcLength(contour, True)
            if perimeter > VisionMap.perimeterMin and perimeter < VisionMap.perimeterMax:
                
                '''edge number'''
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)jjjj
                if len(approx) == 6 or len(approx) == 7 or len(approx) == 8:

                    '''Diagaonal rectangle stuff'''
                    rect = cv2.minAreaRect(contour)
                    '''box = cv2.boxPoints(rect)
                    box = numpy.int0(box)
                    outImage = cv2.drawContours(origImage, [box], 0,(255,0,255), 3)'''
                    #cv2.imshow('Rotated rectangle', outImage)
                    ((x, y), (oldW, oldH), r) = rect
                    if oldW < oldH:
                        w = oldH
                        h = oldW
                    else:
                        w = oldW
                        h = oldH
                    if h < VisionMap.maxHeight and w < VisionMap.maxWidth and h > VisionMap.minHeight and w > VisionMap.minWidth:

                        '''width/heigh ratio'''
                        if float(w)/float(h) < VisionMap.whRatioMax and float(w)/float(h) > VisionMap.whRatioMin:
                            #print(str(2*w + 2*h), "PERIMETER:", str(perimeter/(2*w + 2*h)))
                            
                            '''perimeter ratio'''
                            #print("yay 2")
                            if perimeter / (2*w + 2*h) < VisionMap.perimeterRatioMax and perimeter / (2*w + 2*h) > VisionMap.perimeterRatioMin:
                                #box = cv2.boxPoints((x, y), (w, h), r)
                                #box = np.int0(box)
                                #rectangle = cv2.drawContours(outImage, [box], 0, (255, 0, 255), 2)
                                #cv2.imshow("Rotated Rectangle", outImage)
                                contoursFinal.append([x,y,w,h, True, (w*h*-1)])
    #cv2.waitKey(1)
    contoursFinal.sort(key=lambda x: int(x[5]))
    return outImage, contoursFinal

def makeNetworkTable(IP):
    NetworkTable.setIPAddress(IP)
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    return NetworkTable.getTable("vision")

def HSVthresholdSlider():
    stream = PiVideoStream().start()
    
    cv2.namedWindow('HSV threshold slider')
    cv2.createTrackbar('hLow', 'HSV threshold slider', 0, 180, nothing)
    cv2.createTrackbar('hHigh', 'HSV threshold slider', 0, 180, nothing)
    cv2.createTrackbar('sLow', 'HSV threshold slider', 0, 255, nothing)
    cv2.createTrackbar('sHigh', 'HSV threshold slider', 0, 255, nothing)
    cv2.createTrackbar('vLow', 'HSV threshold slider', 0, 255, nothing)
    cv2.createTrackbar('vHigh', 'HSV threshold slider', 0, 255, nothing)

    while(True):
        image = stream.read()
        cv2.imshow('HSV threshold slider', image)
        hLow = cv2.getTrackbarPos('hLow', 'HSV threshold slider')
        hHigh = cv2.getTrackbarPos('hHigh', 'HSV threshold slider')
        sLow = cv2.getTrackbarPos('sLow', 'HSV threshold slider')
        sHigh = cv2.getTrackbarPos('sHigh', 'HSV threshold slider')
        vLow = cv2.getTrackbarPos('vLow', 'HSV threshold slider')
        vHigh = cv2.getTrackbarPos('vHigh', 'HSV threshold slider')
        hsvLower = numpy.array([hLow, sLow, vLow])
        hsvUpper = numpy.array([hHigh, sHigh, vHigh])
        cv2.imshow("original", image)
        image = cv2.GaussianBlur(image, VisionMap.blur, 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = cv2.inRange(image, hsvLower, hsvUpper)
        cv2.imshow("hsv", image)
        cv2.waitKey(1)

def main():
    #HSVthresholdSlider()
    lastTime = 0

    #create NetworkTable
    table = makeNetworkTable(VisionMap.roboRIOIP)
    table.putNumber("centerX", -1)
    table.putNumber("centerY", -1)
    table.putNumber("width", -1)
    table.putBoolean("Found", False)

    #Start stream
    stream = PiVideoStream().start()
    time.sleep(2)
    
    print("started")
    
    while(True):
        #startTime = time.time()
        image = stream.read()
        _, contours = processImage(image)
        try:
            table.putBoolean("Found", True)
            table.putNumber("centerX", (contours[0][0]-VisionMap.centerY)) #use y because camera rotated
            table.putNumber("centerY", (contours[0][1]-VisionMap.centerX)) #use x because rotated
            table.putNumber("width", contours[0][3]) #use height, because it's rotated sideways
            print("Pushed to NetworkTables")
        except IndexError:
            table.putBoolean("Found", False)
        #lastTime = time.time()
        #print(time.time() - startTime)

if __name__ == "__main__":
    main()
