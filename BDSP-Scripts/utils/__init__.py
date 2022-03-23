""" Import all functions in all modules stored in utils folder"""
import importlib
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
modules = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')] 

# # Mannually add NintendoSwitchAPI module, as it only contains a class
# importlib.import_module("utils.NintendoSwitchAPI")
# # Remove NintendoSwitchApi from the list of modules
# modules.remove('NintendoSwitchAPI')

for module in modules:
    # Import the module
    mod = importlib.import_module('utils.'+module)

    """
    - Add all functions to this module
    - https://stackoverflow.com/questions/31306469/import-from-module-by-importing-via-string/31306598#31306598
    """
    # Determine a list of names to copy to the current name space
    names = getattr(mod, '__all__', [n for n in dir(mod) if not n.startswith('_')])

    # Copy those names into the current name space
    g = globals()
    for name in names:
        g[name] = getattr(mod, name)

