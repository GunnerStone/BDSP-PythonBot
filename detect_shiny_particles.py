""" Inspired by https://github.com/ahoucbvtw/RegiFamily_shiny"""
""" Detecting multiple bright spots in an image with Python and OpenCV """
# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
from torch import hinge_embedding_loss

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to the image file")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it
img = cv2.imread(args["image"])

m1 = cv2.resize(img, (1280, 720))
# m2 = m1[250:500,805:1068]
m2 = m1[0:600,605:1168]
m3 = m1[520:580,120:500]
m1 = m1[0:600,605:1168]

m1 = cv2.inRange(m1, (240,240,240),(255,255,255))
m1 = cv2.dilate(m1, np.ones((30,23)))
contours, hierarchy = cv2.findContours(m1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

print(len(contours))
print(len(hierarchy))
cv2.imshow('img', img)
cv2.imshow('m1', m1)
cv2.imshow('m2', m2)
cv2.imshow('m3', m3)
cv2.waitKey(0)