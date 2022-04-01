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
    logging.debug("Topping off Theif PP at pokecenter")
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)

    # wait for the pokewatch to disappear
    while utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # wait for the pokewatch to reappear
    while not utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # walk to the nurse joy
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Left'].lower(),0.1).wait(0.2)

    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.1).wait(0.2)

    # press A until the pokewatch dissapears
    while utils.has_pokewatch_btn_screen(driver):
        driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
    
    # when the pokewatch dissapears, press a once
    time.sleep(0.2)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
    
    # press B until the pokewatch reappears
    while not utils.has_pokewatch_btn_screen(driver):
        driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)

    # leave the pokecenter
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)

    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Right'].lower(),0.1).wait(0.2)

    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)

    # wait for the pokewatch to disappear
    while utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # wait for the pokewatch to reappear
    while not utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # walk to water
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1).wait(0.2)

    def use_rod():
        logging.debug("Using Fishing Rod")

        driver.hold_key(controller['Key_Start'].lower(),0.2).wait(0.5)
        driver.hold_key(controller['Key_Dpad_Left'].lower(),0.2).wait(0.5)

    def locate_fish_alert_on_screen():
        img = driver.screenshot_RAM()
        # convert to opencv
        img = np.array(img)
        img = cv2.resize(img, (1280, 720))

        # take a crop of the inner portion of the screen
        img = img[220:500,300:900]

        if driver.match_image(img, "BDSP-Scripts/assets/fish_alert.png", threshold=0.01):
            return True
        else:
            return False
    
    def locate_failed_fish_alert_on_screen():
        img = driver.screenshot_RAM()
        # convert to opencv
        img = np.array(img)
        img = cv2.resize(img, (1280, 720))

        # take a crop of the inner portion of the screen
        img = img[500:700,200:900]

        if driver.match_image(img, "BDSP-Scripts/assets/battle_text.png", threshold=0.01):
            return True
        else:
            return False

    def check_for_fish():
        use_rod()
        # check for vs seeker alert until pokewatch reappears
        logging.debug("Scanning for Fish Alert on screen")

        while True:
            if locate_fish_alert_on_screen():
                found_fight_flag = True
                logging.debug("Fish Alert found on screen")
                break
            if locate_failed_fish_alert_on_screen():
                logging.debug("Did not find a fish... pressing B to continue")
                time.sleep(0.5)
                driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.4)
                found_fight_flag = False
                break
        return found_fight_flag

    num_PP = 40 # how many fights to do
    while num_PP > 0:
        logging.debug("Starting VS Seeker Loop with PP: {}".format(num_PP))
        if check_for_fish():
            # press A to hook fish!
            driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
            
            logging.debug("Found a fish! Pressing A to continue")
            time.sleep(1.5)
            # press A to continue to fight
            driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)

            """ FISH HOOKED """
            logging.debug("Looking for white-screen trigger")
            # looks for white screen
            while not utils.has_white_screen(driver):
                time.sleep(0.1)

            while utils.has_white_screen(driver):
                time.sleep(0.1)

            logging.debug("Looking for shiny animation")

            # check if shiny
            while not utils.has_battletext_screen(driver):
                time.sleep(0.1)
            time_check = time.time()

            while utils.has_battletext_screen(driver):
                time.sleep(0.1)

            # if it's shiny, wait for the battle text screen to appear much later than usual
            while not utils.has_battletext_screen(driver):
                time.sleep(0.1)
            time_check_2 = time.time()

            # logging.debug the time difference in seconds
            logging.debug("Time difference: " + str(time_check_2 - time_check))

            # check to see if its shiny
            if time_check_2 - time_check > gc.shiny_timing_threshold:
                # quit the program
                time.sleep(10)
                curr_pokemon = str(utils.get_enemy_pokemon_name(driver)).upper().strip()
                utils.found_shiny_text(curr_pokemon)
                quit()
            
            logging.debug("Did NOT detect shiny")

            # wait for run button to appear
            while not utils.has_run_btn(driver):
                time.sleep(0.5)
            
            logging.debug("Run button found")
            
            
            """ Check to see if its a desirable pokemon """
            desired_pokemon = ["LUVDISC","LUVDISE"]

            time.sleep(1)
            # check if the pokemon is in the desired list
            curr_pokemon = str(utils.get_enemy_pokemon_name(driver)).upper().strip()
            logging.debug("Current Pokemon: " + curr_pokemon)

            IS_CATCHING = False
            if curr_pokemon in desired_pokemon:
                logging.debug("Found " + curr_pokemon + " in battle")
                IS_CATCHING = True
            
            if IS_CATCHING:
                num_PP -= 1
                """ Press A until battle is over """
                while not utils.has_black_screen(driver):
                    driver.hold_key(controller['Key_A'].lower(),0.2)
            else:
                """ Flee from battle """
                driver.hold_key(controller['Key_Dpad_Up'],0.2).wait(0.2)

                """ Press A until battle is over """
                while not utils.has_black_screen(driver):
                    driver.hold_key(controller['Key_A'].lower(),0.2)

            logging.debug("Battle is Over...")
            # press B until the battle is over
            while not utils.has_pokewatch_btn_screen(driver):
                driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)

            # Battle is over, remove the item from first pokemon if its a luvdisc
            if IS_CATCHING:
                driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.4)
                driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.8)
                driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
                driver.hold_key(controller['Key_Dpad_Up'].lower(),0.2).wait(0.2)
                driver.hold_key(controller['Key_Dpad_Up'].lower(),0.2).wait(0.2)
                driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
                driver.hold_key(controller['Key_Dpad_Down'].lower(),0.2).wait(0.2)
                driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
                # press B until the pokewatch appears
                while not utils.has_pokewatch_btn_screen(driver):
                    driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)
            time.sleep(1)
            # cls the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

    return