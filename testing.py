from NintendoSwitchAPI import *
import time
from threading import Thread
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
import sys
from xml.etree import cElementTree as ElementTree
import ControllerMapping
import os

# how many seconds until the program takes control of the controller
leeway = 10

try:
    print ("You have {} seconds to Enable Capture Mode on the MaxAim Di controller".format(leeway))
    time.sleep(leeway)

    driver = NintendoSwitchAPI().register_window(name="4K Capture Utility", nth=0)
    wx, wy = driver.get_window_rect()[:2]

    print("4K Capture Utility found successfully!")

    
    controller = ControllerMapping.getController()
    print("Controller Config: {} found successfully!".format(controller["@name"]))
    del controller["@name"]

    

    def controller_test():
        for key in controller:
            curr_button = controller[key].lower()
            print("Pressing {}".format(curr_button))
            if curr_button == '`':
                continue
            pydirectinput.keyDown(curr_button)
            pydirectinput.keyUp(curr_button)
            # driver.hold_key(curr_button)
            time.sleep(0.5)

    try:
        while True:
            controller_test()

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

