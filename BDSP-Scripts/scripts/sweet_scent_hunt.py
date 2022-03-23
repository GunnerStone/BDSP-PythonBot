# sweet_scent_hunt.py
"""
- This script is used to hunt for shiny wild pokemon
- It will hunt for a shiny wild pokemon until it finds one
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
    logging.debug("Looking for battle trigger")

    """ Use sweet scent to start battle """
    driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.4)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.8)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.2)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.1)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1)
    driver.hold_key(controller['Key_A'].lower(),0.1)


    logging.debug("Looking for white-screen trigger")
    # looks for white screen
    while not utils.has_white_screen(driver):
        time.sleep(0.1)

    while utils.has_white_screen(driver):
        time.sleep(0.1)

    # TBD - timer for shiny animation
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

    if time_check_2 - time_check > 3.1:
        # quit the program
        quit()
    
    logging.debug("Did NOT detect shiny")

    # wait for run button to appear
    while not utils.has_run_btn():
        time.sleep(0.5)
    
    logging.debug("Run button found")
    
    
    """ Check to see if its a desirable pokemon """
    desired_pokemon = gc.target_pokemon

    IS_CATCHING = False
    
    # check if the pokemon is in the desired list
    curr_pokemon = str(utils.get_enemy_pokemon_name(driver)).upper().strip()
    logging.debug("Current Pokemon: " + curr_pokemon)

    if curr_pokemon in desired_pokemon:
        logging.debug("Found " + curr_pokemon + " in battle")
        IS_CATCHING = True
    
    if IS_CATCHING:
        driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.5)
        driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.5)

    """ Flee from battle """
    driver.hold_key(controller['Key_Dpad_Up'],0.2).wait(0.2)

    """ Press A until battle is over """
    while not utils.has_black_screen(driver):
        driver.hold_key(controller['Key_A'].lower(),0.2)

    logging.debug("Battle is Over...")
    # battle is over
    while not utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.5)

    return