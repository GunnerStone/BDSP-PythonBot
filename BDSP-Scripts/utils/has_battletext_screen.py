import numpy as np
import cv2

def has_battletext_screen(driver):
    # takes a screenshot of the game
    img = driver.screenshot_RAM()

    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[640:660,705:1068] # battle_text screen

    if driver.match_image(img, "./assets/battle_text.png", threshold=0.1):
        return True
    else:
        return False