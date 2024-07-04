"""
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)

"""

from pypylon import pylon
import cv2 as cv
import numpy as np


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
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        var = int(input("num:"))

        """thres = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        thres = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        (T, thresh) = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)

        thres = cv2.bitwise_not(thres)"""
        # apply normal and adaptive thresholding to the image
        ret, thresh = cv.threshold(gray, var, 255, cv.THRESH_BINARY)
        adapt = cv.adaptiveThreshold(
            gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 99, var
        )
        # create resizable windows for the images to be displayed
        cv.namedWindow("adapt", cv.WINDOW_NORMAL)
        cv.namedWindow("thresh", cv.WINDOW_NORMAL)
        # show the image
        cv.imshow("thresh", thresh)
        cv.imshow("adapt", adapt)
        k = cv.waitKey(1)
        if k == 27:
            break

    grabResult.Release()

# Releasing the resource
camera.StopGrabbing()


cv.destroyAllWindows()

import os
