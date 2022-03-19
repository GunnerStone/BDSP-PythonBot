""" Inspired by https://github.com/ahoucbvtw/RegiFamily_shiny"""
""" Detecting multiple bright spots in an image with Python and OpenCV """
# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

def get_contour_count(img):
    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #     help="path to the image file")
    # args = vars(ap.parse_args())

    # # load the image, convert it to grayscale, and blur it
    # img = cv2.imread(args["image"])

    # verify resolution is 720p
    if type(img) is not np.ndarray:
        img = np.array(img)
        img = img[:,:,::-1].copy()
    m1 = cv2.resize(img, (1280, 720))

    # crop image to only show the enemy pokemon
    m2 = m1[610:660,965:1068] # run_btn screen
    # m2 = m1[640:660,705:1068] # battle_text screen
    # m2 = m1[70:250,1140:1180] #pokewatch screen
    cv2.imwrite("m2.png", m2)
    m3 = m1[520:580,120:500]
    m1 = m1[0:600,605:1168]

    m1 = cv2.inRange(m1, (240,240,240),(255,255,255))
    m1 = cv2.dilate(m1, np.ones((30,23)))
    contours, hierarchy = cv2.findContours(m1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cv2.imshow('img', img)
    cv2.imshow('m1', m1)
    cv2.imshow('m2', m2)
    cv2.imshow('m3', m3)
    cv2.waitKey(0)