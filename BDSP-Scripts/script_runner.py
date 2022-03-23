# testing.py
""" 
- This python script runs the user-specified script in Config_Files/global_config.py
"""
import time
import sys
import os

""" import necessary util functions """
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent directory to path
import utils
from scripts import *
import Config_Files.global_config as gc

try:
    # Look for a running instance of a capture utility (defined in the Config_Files/global_config.py file)
    driver = utils.NintendoSwitchAPI().register_window(name=gc.capture_utility_name, nth=0)
    wx, wy = driver.get_window_rect()[:2]

    print("{} found successfully!".format(gc.capture_utility_name))

    print ("You have {} seconds to Enable Capture Mode on the MaxAim Di controller".format(gc.leeway))
    time.sleep(gc.leeway)
    
    controller = utils.getController()
    print("Controller Config: {} found successfully!".format(controller["@name"]))
    del controller["@name"]
    
    try:
        while True:
            """ Run the script that is defined in the Config_Files/global_config.py file """
            # load a module dynamically from the scripts folder
            # and launch the 'run' function from that module
            # from https://stackoverflow.com/questions/17142090/how-to-get-reference-to-module-by-string-name-and-call-its-method-by-string-name
            getattr(globals()[gc.running_script_name],'run')(driver,controller)

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
