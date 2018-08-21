""" Script to run all the API Calls using IR-Flow Client against an IR-Flow API endpoint"""
import uuid
import datetime
import logging
import os
import pprint
import irflow_client
import sys


pp = pprint.PrettyPrinter(indent=4)
# The first thing any script does is instantiate the irflow_api client library.
# NOTE: We pass the configuration file to the library when we instantiate it.
# The configuration file specifies the
# irflow end point, user, and API Key, as well as the debug flag.
config_file = "irflow_api.conf"

if os.path.exists(config_file):
    # setup irflow Client
    irflowAPI = irflow_client.IRFlowClient(config_file=config_file)
else:
    print('path to irflow_api.conf file is not found')
    sys.exit(1)

if irflowAPI.debug:
    # If debug information is desired, create a simple logging config that sets the default
    # lowest printed level to DEBUG
    logging.basicConfig(level=logging.DEBUG)
else:
    # otherwise, use the standard configuration of the INFO level - these logging configurations can be made much
    # more complex, but this sort of configuration is the minimum needed to get output on the console. If you're using
    # the irflow-integrations package, a package wide logging configuration can be found in the
    # irflow_integrations.utils submodule
    logging.basicConfig(level=logging.INFO)

# Once the logger has been configured, create the logger instance for this class. Even though the code in this example
# uses only print statements for console output, a logging object must be made in order for the logging information from
# the irflow_client object to be output
logger = logging.getLogger('IR-Flow API Example')

if irflowAPI.debug:
    # Now that a logger has been created, we can dump the settings of the client if the debug flag is set, or skip this
    # otherwise.
    irflowAPI.dump_settings()

print('=========== Get IR-Flow Version =========')
try:
    version = irflowAPI.get_version()
except ConnectionError:
    print('Something went wrong')

print(version)

incident_data = irflowAPI.update_incident(1, None, "ET Incident Type", None, None)
pp.pprint(incident_data)