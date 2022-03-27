import numpy as np
import cv2
import os
def has_battletext_screen(driver,threshold=0.1):
    # takes a screenshot of the game
    img = driver.screenshot_RAM()

    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[640:660,705:1068] # battle_text screen

    if driver.match_image(img, "BDSP-Scripts/assets/battle_text.png", threshold):
        return True
    else:
        return False