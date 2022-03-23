import numpy as np
import cv2

def has_run_btn(driver):
    # takes a screenshot of the game
    img = driver.screenshot_RAM()
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[610:660,965:1068]

    if driver.match_image(img, "./assets/run_btn.png", threshold=0.1):
        return True
    else:
        return False