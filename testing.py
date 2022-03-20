from NintendoSwitchAPI import *
import time
from threading import Thread
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
import sys
from xml.etree import cElementTree as ElementTree
import ControllerMapping
import os
import numpy as np

#custom libraries
from NintendoSwitchAPI import *
from detect_shiny_particles import get_contour_count

# how many seconds until the program takes control of the controller
leeway = 3


def get_enemy_pokemon_name():
    # takes a screenshot of the game
    img = driver.screenshotRAM()

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

def has_pokewatch_btn_screen():
    # takes a screenshot of the game
    img = driver.screenshotRAM()
    
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[70:250,1140:1180] # pokewatch screen

    if driver.match_image(img, "./assets/pokewatch_btn.png", threshold=0.1):
        return True
    else:
        return False

def has_battletext_screen():
    # takes a screenshot of the game
    img = driver.screenshotRAM()

    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[640:660,705:1068] # battle_text screen

    if driver.match_image(img, "./assets/battle_text.png", threshold=0.1):
        return True
    else:
        return False

def has_run_btn():
    # takes a screenshot of the game
    img = driver.screenshotRAM()
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))

    img = img[610:660,965:1068]

    if driver.match_image(img, "./assets/run_btn.png", threshold=0.1):
        return True
    else:
        return False



def has_white_screen():
    # takes a screenshot of the game
    img = driver.screenshotRAM()
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))
    img = img[0:600,605:1168]
    # if a large majority of the image is white, return true
    if cv2.mean(img)[0] > 240:
        return True
    else:
        return False

def has_black_screen():
    # takes a screenshot of the game
    img = driver.screenshotRAM()
    # convert to opencv
    img = np.array(img)
    img = cv2.resize(img, (1280, 720))
    img = img[0:600,605:1168]
    # if a large majority of the image is black, return true
    if cv2.mean(img)[0] < 15:
        return True
    else:
        return False

def get_in_battle():
    # looks for battle trigger
    print("Looking for battle trigger")

    """ Run left & right until fight loop"""
    # while True:
    #     # moves up and down by 1 square at a time
    #     driver.hold_key(controller['Key_Dpad_Left'],0.2)
    #     if not has_pokewatch_btn_screen():
    #         break

    #     driver.hold_key(controller['Key_Dpad_Right'],0.2)
    #     if not has_pokewatch_btn_screen():
    #         break

    """ Use sweet scent to start battle """
    driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.4)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.8)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.2)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.1)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1)
    driver.hold_key(controller['Key_A'].lower(),0.1)


    print("Looking for white-screen trigger")
    # looks for white screen
    while not has_white_screen():
        time.sleep(0.1)

    while has_white_screen():
        time.sleep(0.1)

    # TBD - timer for shiny animation
    print("Looking for shiny animation")

    # check if shiny
    while not has_battletext_screen():
        time.sleep(0.1)
    time_check = time.time()

    while has_battletext_screen():
        time.sleep(0.1)

    # if it's shiny, wait for the battle text screen to appear much later than usual
    while not has_battletext_screen():
        time.sleep(0.1)
    time_check_2 = time.time()

    # print the time difference in seconds
    print("Time difference: " + str(time_check_2 - time_check))
    time_diff = str(time_check_2 - time_check)
    my_logfile = open("logfile.txt", "a")
    my_logfile.write(time_diff + "\n")
    my_logfile.close()

    if time_check_2 - time_check > 3.1:
        # quit the program
        quit()
    
    print("Did NOT detect shiny")

    # wait for run button to appear
    while not has_run_btn():
        time.sleep(0.5)
    
    print("Run button found")
    
    
    """ Check to see if its a desirable pokemon """
    desired_pokemon = ["ABRA"]

    IS_CATCHING = False
    
    # check if the pokemon is in the desired list
    curr_pokemon = str(get_enemy_pokemon_name()).upper().strip()
    print("Current Pokemon: " + curr_pokemon)

    if curr_pokemon in desired_pokemon:
        print("Found " + curr_pokemon + " in battle")
        IS_CATCHING = True
    
    if IS_CATCHING:
        driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.5)
        driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.5)
    """ Flee from battle """
    driver.hold_key(controller['Key_Dpad_Up'],0.2).wait(0.2)
    """ Press A until battle is over """
    while not has_black_screen():
        driver.hold_key(controller['Key_A'].lower(),0.2)

    # # looks for black screen
    # print("Looking for black-screen trigger")
    # while not has_black_screen():
    #     time.sleep(0.1)

    print("Battle is Over...")
    # battle is over
    while not has_pokewatch_btn_screen():
        time.sleep(0.5)

    return

def dialga_shiny_hunt():
    # looks for battle trigger
    print("Walking into battle")
    driver.hold_key(controller['Key_Dpad_Up'],0.2).wait(0.2)

    # press A until the white screen appears
    while not has_white_screen():
        driver.hold_key(controller['Key_A'].lower(),0.2)
        time.sleep(0.1)

    while has_white_screen():
        time.sleep(0.1)

    # TBD - timer for shiny animation
    print("Looking for shiny animation")

    # check if shiny
    while not has_battletext_screen():
        time.sleep(0.1)
    print("Grabbed checkpoint time A")
    time_check = time.time()

    while has_battletext_screen():
        time.sleep(0.1)

    # if it's shiny, wait for the battle text screen to appear much later than usual
    while not has_battletext_screen():
        time.sleep(0.1)
    print("Grabbed checkpoint time B")
    time_check_2 = time.time()

    # print the time difference in seconds
    print("Time difference: " + str(time_check_2 - time_check))
    time_diff = str(time_check_2 - time_check)
    my_logfile = open("logfile.txt", "a")
    my_logfile.write(time_diff + "\n")
    my_logfile.close()

    if time_check_2 - time_check > 2.1:
        # quit the program
        quit()
    
    print("Did NOT detect shiny")

    print("Resetting game")
    """ Reset the game """
    driver.hold_key(controller['Key_Home'],0.2).wait(0.7)
    driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.5)
    
    # press A until pokewatch btn appears
    while not has_pokewatch_btn_screen():
        driver.hold_key(controller['Key_A'].lower(),0.2)
        driver.hold_key(controller['Key_RB'].lower(),0.2)
        time.sleep(0.5)

    return



try:
    

    driver = NintendoSwitchAPI().register_window(name="4K Capture Utility", nth=0)
    wx, wy = driver.get_window_rect()[:2]

    print("4K Capture Utility found successfully!")

    print ("You have {} seconds to Enable Capture Mode on the MaxAim Di controller".format(leeway))
    time.sleep(leeway)
    
    controller = ControllerMapping.getController()
    print("Controller Config: {} found successfully!".format(controller["@name"]))
    del controller["@name"]
    

    def controller_test():
        for key in controller:
            curr_button = controller[key].lower()
            if key == "Key_Dpad_Up":
                print("Pressing {}".format(curr_button))
                if curr_button == '`':
                    continue
                driver.hold_key(controller[key],0.2)
                # driver.hold_key(curr_button)
                time.sleep(0.5)

    def get_pokemon_contour_count():
        # take a screenshot of the game
        screenshot = driver.screenshotRAM()
        # get the contour count
        return get_contour_count(screenshot)

    try:
        while True:
            # controller_test()
            # num_contours = get_pokemon_contour_count()
            # print(get_enemy_pokemon_name())
            # print("Numbera of Enemy Pokemon Contours: {}".format(num_contours))
            # get_in_battle()
            dialga_shiny_hunt()
            # hehe_screenshot = driver.screenshotRAM()
    except KeyboardInterrupt:
            print ('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
except Exception as e:
    print(e)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

