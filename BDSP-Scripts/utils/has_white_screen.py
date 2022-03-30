import numpy as np
import cv2

def has_white_screen(driver):
    # takes a screenshot of the game
    img = driver.screenshot_RAM()
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))
    img = img[50:550, 655:1118]
    
    # if a large majority of the image is white, return true
    return cv2.mean(img)[0] > 240