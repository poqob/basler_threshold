"""
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)

"""
import cv2
import cv2 as cv
from pypylon import pylon

from pyimagesearch import imutils

var = 9  # int(input("num:"))
var0 =99

def getvar():
    return var
def getvar0():
    return var0

def setvar(val):
    global var
    var = int(val)

def setvar0(val):
    global var
    var = int(val)

def run():
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            # cv.namedWindow("img", cv.WINDOW_NORMAL)
            # cv.imshow("img", mat=img)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)


            # apply normal and adaptive thresholding to the image
            ret, thresh = cv.threshold(blurred, var, 255, cv.THRESH_BINARY)
            adapt = cv.adaptiveThreshold(
                blurred, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, getvar0(), getvar()
            )
            edged = cv2.Canny(adapt, 30, 150)
            edges = cv2.Canny(adapt, 50, 150, apertureSize=3)
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # How many contours did we find?
            print("I count {} coins in this image".format(len(cnts)))


            # create resizable windows for the images to be displayed
            cv.namedWindow("img", cv.WINDOW_NORMAL)
            cv.namedWindow("adapt", cv.WINDOW_NORMAL)
            cv.namedWindow("thresh", cv.WINDOW_NORMAL)
            cv.namedWindow("Edged", cv.WINDOW_NORMAL)
            cv.namedWindow("Edges", cv.WINDOW_NORMAL)
            cv.namedWindow("Blurred", cv.WINDOW_NORMAL)

            # show the image
            cv.imshow("img", img)
            cv.imshow("thresh", thresh)
            cv.imshow("adapt", adapt)
            cv2.imshow("Edged", edged)
            cv2.imshow("Edges", edges)
            cv2.imshow("Blurred", blurred)



            k = cv.waitKey(1)
            if k == 27:
                break
            # cv2.imwrite('output/adapt.jpg',adapt)
            # cv2.imwrite('output/img.jpg',img)

            # break
        grabResult.Release()

    # Releasing the resource
    camera.StopGrabbing()

    cv.destroyAllWindows()

