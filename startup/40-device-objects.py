import logging
import time
import bluesky.plan_stubs as bps
from ophyd.ophydobj import Kind
from ophyd.signal import EpicsSignal, Signal
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   FormattedComponent as FC)
import csv
from _collections import OrderedDict
import logging.config
from ophyd.status import DeviceStatus
from ophyd.status import wait as status_wait
from deposition_components.DepositionListDevice import DepositionListDevice

# ## Coming lines help define the logging facility
LOGGER_NAME = "mirrorBluesky"
LOGGER_DEFAULT = {
    'version' : 1,
    'handlers' : {'consoleHandler' : {'class' : 'logging.StreamHandler',
                               'level' : 'INFO',
                               'formatter' : 'consoleFormat',
                               'stream' : 'ext://sys.stdout'} ,
                  },
    'formatters' : {'consoleFormat' : {'format' : '%(asctime)-15s - %(name)s - %(funcName)s- %(levelname)s - %(message)s'},
                    },
    'loggers' : {'root' :{'level' : 'INFO',
                        'handlers' : ['consoleHandler', ],
                      },
               LOGGER_NAME : {'level' : 'INFO',
                            'handlers' : ['consoleHandler', ],
                            'qualname' : LOGGER_NAME
                            }
               },
   }

userDir = os.path.expanduser("~")
logConfigFile = os.path.join(userDir, LOGGER_NAME + 'Log.config')
if os.path.exists(logConfigFile):
    print ("logConfigFile " + logConfigFile)
    try:
        logging.config.fileConfig(logConfigFile,
                                  disable_existing_loggers=False)
        print("Success Openning logfile")
    except (NoSectionError, TypeError) as ex:
        print ("In Exception to load dictConfig package %s Because of "
               "exeption\n  %s" % (LOGGER_NAME, ex))
        logging.config.dictConfig(LOGGER_DEFAULT)
    except KeyError as ex:
        print ("logfile %s was missing or had errant sections %s" % 
               (logConfigFile, ex.args))
else:
    logging.config.dictConfig(LOGGER_DEFAULT)
logger = logging.getLogger(LOGGER_NAME)

print("__name__: %s" % __name__)
 
NUMBER_OF_GUNS = 8
CONFIG_FIELDS = ["object", "channel_name", "pv", "write_pv", \
                 "description", "name"]


def testDepositionListDevice():
    dev = DepositionListDevice("test:", instance_number=1, \
                                config_file='pv_map.csv')
    logger.debug (dev.configuration)
    print (dev.__class__)


VALVE_ALL_OPEN = 100.0
VALVE_ALL_CLOSED = 0.000
CCG_ON_VALUE = 1
CCG_OFF_VALUE = 0

