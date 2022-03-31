import time
import sys
import os
import pydirectinput

""" import necessary util functions """
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent directory to path
import utils



def teleport_to_pokecenter_and_heal(driver, controller):
    """ Use teleport from last pokemon in party """
    driver.hold_key(controller['Key_X'].lower(),0.2).wait(0.4)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.8)
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.2)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.1)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.1)
    driver.hold_key(controller['Key_A'].lower(),0.1)

    # wait until the pokewatch appears
    while not utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)
    # go into pokecenter
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.2)

    # wait until theh pokewatch disappears
    while utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # wait until the pokewatch appears
    while not utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # keep b button held down to run
    pydirectinput.keyDown(controller['Key_B'].lower())
    driver.wait(0.2)
    # go up and talk to nurse joy
    driver.hold_key(controller['Key_Dpad_Up'].lower(),0.7).wait(0.3)

    # release b button
    pydirectinput.keyUp(controller['Key_B'].lower())

    # press A until the pokewatch dissapears
    while utils.has_pokewatch_btn_screen(driver):
        driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
    
    # when the pokewatch dissapears, press a once
    time.sleep(0.2)
    driver.hold_key(controller['Key_A'].lower(),0.2).wait(0.2)
    
    # press B until the pokewatch reappears
    while not utils.has_pokewatch_btn_screen(driver):
        driver.hold_key(controller['Key_B'].lower(),0.2).wait(0.2)

    # run down until you leave the pokecenter
    # keep b button held down to run
    pydirectinput.keyDown(controller['Key_B'].lower())
    driver.wait(0.2)
    driver.hold_key(controller['Key_Dpad_Down'].lower(),0.9)

    # release b button
    pydirectinput.keyUp(controller['Key_B'].lower())

    # wait until the pokewatch disappears
    while utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)

    # wait until the pokewatch appears
    while not utils.has_pokewatch_btn_screen(driver):
        time.sleep(0.2)
    
    time.sleep(1)
    print("DONE")

    

    return