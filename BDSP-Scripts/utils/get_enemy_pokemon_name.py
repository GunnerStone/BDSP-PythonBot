import numpy as np
import cv2
import pytesseract

""" 
- Takes in an instance of the NintendoSwitchAPI class
- Assumes the window is already registered
- Returns the name of the enemy pokemon
"""
def get_enemy_pokemon_name(driver):
    # takes a screenshot of the game
    img = driver.screenshot_RAM()

    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[100:130,900:1068] # pokemon name box

    # filter out all pixels that arent very close to black
    img = cv2.inRange(img, (0,0,0), (100,100,100))

    # flip the black and white
    img = cv2.bitwise_not(img)

    # read using tesseract
    text = pytesseract.image_to_string(img)

    return text