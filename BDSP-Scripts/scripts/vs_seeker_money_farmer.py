# sweet_scent_hunt.py
"""
- This script is used to hunt for shiny wild pokemon
- It will hunt for a shiny wild pokemon until it finds one
"""
import time
import sys
import os
import logging

import pydirectinput
import numpy as np
import cv2

""" import necessary util functions """
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent directory to path
import Config_Files.global_config as gc
import utils

def run(driver, controller):
    logging.basicConfig(stream=sys.stderr, level=gc.Logging_Level)

    """ Restore PP of all moves"""
    logging.debug("Topping off at pokecenter")
    utils.teleport_to_pokecenter_and_heal(driver, controller)

    # enable running by pressing B down
    pydirectinput.keyDown(controller['Key_B'])
    time.sleep(0.1)
    """ Navigate out of hearthstone"""
    driver.hold_key(controller['Key_Dpad_Down'].lower(),2.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),2.9).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),2.4).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),3.9).wait(0.2)

    """ Navigate to the old couple """
    # Navigate through the forest
    driver.hold_key(controller['Key_Dpad_Down'].lower(),11.0).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.8).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),1.2).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),1.5).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.5).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.8).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),1.6).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),2.2).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),1.2).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.8).wait(0.2)#needs to be exact
    driver.hold_key(controller['Key_Dpad_Down'].lower(),2.8).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),1.5).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),2.9).wait(0.2)

    def charge_vs_seeker():
        for i in range(0,6):
            driver.hold_key(controller['Key_Dpad_Left'].lower(),1.8)
            driver.hold_key(controller['Key_Dpad_Right'].lower(),1.8).wait(0.2)

    def use_vs_seeker():
        driver.hold_key(controller['Key_Start'].lower(),0.2).wait(0.5)
        driver.hold_key(controller['Key_Dpad_Down'].lower(),0.2).wait(0.5)

    def locate_vs_seeker_alert_on_screen():
        img = driver.screenshot_RAM()
        # convert to opencv
        img = np.array(img)
        img = cv2.resize(img, (1280, 720))

        # take a crop of the inner portion of the screen
        img = img[120:600,300:900]

        if driver.match_image(img, "BDSP-Scripts/assets/vs_seeker_alert.png", threshold=0.05):
            return True
        else:
            return False

    def check_for_fight():
        charge_vs_seeker()
        time.sleep(1)
        use_vs_seeker()
        found_fight_flag = False
        # check for vs seeker alert until pokewatch reappears
        while not utils.has_pokewatch_btn_screen(driver):
            if locate_vs_seeker_alert_on_screen():
                found_fight_flag = True
            # press B to continue
            driver.hold_key(controller['Key_B'].lower(),0.2)
        time.sleep(2)
        return found_fight_flag

    num_PP = 30 # how many fights to do
    while num_PP > 0:
        if check_for_fight():
            num_PP -= 1
            # walk to the left and fight the vs seeker
            # release the b button
            pydirectinput.keyUp(controller['Key_B'])
            time.sleep(0.1)
            driver.hold_key(controller['Key_Dpad_Left'].lower(),0.6).wait(0.2)
            driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
            # press A until the pokewatch disappears
            while utils.has_pokewatch_btn_screen(driver):
                driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)

            # press A until the pokewatch reappears
            while not utils.has_pokewatch_btn_screen(driver):
                driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
            
            # remove dialogue with the vs seeker
            driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)
            driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)
            driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)
        #enable run
        pydirectinput.keyDown(controller['Key_B'])
        time.sleep(1)

    return