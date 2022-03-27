# global_config.py
# """
# Logging Levels:
# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0
import logging
Logging_Level = logging.DEBUG

# leeway: how long the user has to enable capture mode on the MaxAim Di controller
leeway = 3.0

capture_utility_name = "4K Capture Utility"
running_script_name = "stationary_legendary_hunt"

# timing threshold for a shiny animation
shiny_timing_threshold = 3.1

controller_config_profile_name = "BDSP"

# list of target pokemon to hunt for
# used to catch pokemon that are not shiny in scripts/sweet_scent_hunt.py
target_pokemon = ['ABRA']