import numpy

#magic numbers
#camera settings
resolution = (320, 240)
centerX = 160#resolution[0]/2
centerY = 120#resolution[1]/2
framerate = 15
exposure = 150#200#1250
brightness = 45
sharpness = 50
saturation = 50
framerate = 32
rotation = 180
exposureMode = 'off'

#processing settings
hsvLower = numpy.array([25, 80, 60])
hsvUpper = numpy.array([110, 255, 255])
#hsvLower = numpy.array([41, 171, 30])
#hsvUpper = numpy.array([119, 255, 255])
#hsvLower = numpy.array([40, 90, 35])
#hsvUpper = numpy.array([165, 255, 251])
#hsvLower = numpy.array([0, 30, 15])
#hsvUpper = numpy.array([180, 255, 250])
blur = 1
cannyThreshMin = 10
cannyThreshMax = 250 #TODO test these numbers
areaMin = 175
areaMax = 4000
perimeterMin = 100
perimeterMax = 1000
imageNum = 3
imagePath = "sample" + str(imageNum) + ".jpg"

roboRIOIP = "roborio-4613-frc.local"
whRatioMax = 2.3
whRatioMin = 1.45
perimeterRatio = float(4.0/5.5)
perimeterRatioMax = 1.3
perimeterRatioMin = 1.18
minHeight = 18
maxHeight = 150
minWidth = 28
maxWidth = 250
