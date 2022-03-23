# box_art_legendary_hunt.py
"""
- This script is used to hunt for shiny legendary pokemon
- It will hunt for a shiny legendary pokemon until it finds one
- 
- Legendary pokemon must be stationary (ie. not moving) and must
- not respond to movement triggers
-
- Must have game saved facing legendary pokemon
"""
import time
import sys
import os
import logging

""" import necessary util functions """
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent directory to path
import Config_Files.global_config as gc
import utils

def run(driver, controller):
    logging.basicConfig(stream=sys.stderr, level=gc.Logging_Level)

    # looks for battle trigger
    logging.debug("Walking into battle")
    driver.hold_key(controller['Key_Dpad_Up'],0.2).wait(0.2)

    # press A until the white screen appears
    while not utils.has_white_screen(driver):
        driver.hold_key(controller['Key_A'].lower(),0.2)
        time.sleep(0.1)

    while utils.has_white_screen(driver):
        time.sleep(0.1)

    # TBD - timer for shiny animation
    logging.debug("Looking for shiny animation")

    # check if shiny
    while not utils.has_battletext_screen(driver):
        time.sleep(0.1)
    logging.debug("Grabbed checkpoint time A")
    time_check = time.time()

    while utils.has_battletext_screen(driver):
        time.sleep(0.1)

    # if it's shiny, wait for the battle text screen to appear much later than usual
    while not utils.has_battletext_screen(driver):
        time.sleep(0.1)
    logging.debug("Grabbed checkpoint time B")
    time_check_2 = time.time()

    # logging.debug the time difference in seconds
    logging.debug("Time difference: " + str(time_check_2 - time_check))
    time_diff = str(time_check_2 - time_check)
    my_logfile = open("logfile.txt", "a")
    my_logfile.write(time_diff + "\n")
    my_logfile.close()

    if time_check_2 - time_check > 2.1:
        # quit the program
        quit()
    
    logging.debug("Did NOT detect shiny")

    logging.debug("Resetting game")
    """ Reset the game """
    driver.hold_key(controller['Key_Home'],0.2).wait(0.7)
    driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.5)
    
    # press A until pokewatch btn appears
    while not utils.has_pokewatch_btn_screen(driver):
        driver.hold_key(controller['Key_A'].lower(),0.2)
        driver.hold_key(controller['Key_RB'].lower(),0.2)
        time.sleep(0.5)

    return