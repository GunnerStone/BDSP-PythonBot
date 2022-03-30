import numpy as np
import cv2

def has_pokewatch_btn_screen(driver):
    # takes a screenshot of the game
    img = driver.screenshot_RAM()
    
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[150:250,1140:1180] # pokewatch screen
    if driver.match_image(img, "BDSP-Scripts/assets/pokewatch_btn.png", threshold=0.1):
        return True
    else:
        return False