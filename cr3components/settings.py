from cr3components import GlobalSettings
import os
gs = GlobalSettings()

#following 3 variables are required by defaults
gs["PROJECT"] = "cr3components"
gs["DBPASS"] = ""
gs["SECRET_KEY"] = ""

gs["ROOT_PATH"] = os.path.dirname(__file__)

try:
    from cr3components.defaults import *
except ImportError:
    try:
        from .defaults import * #just for cr3components project
    except ImportError:
        print "No defaults configured"

#Begin of project related settings
