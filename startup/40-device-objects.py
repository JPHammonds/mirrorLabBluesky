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

### Coming lines help define the logging facility
LOGGER_NAME="mirrorBluesky"
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
                        'handlers' : ['consoleHandler',],
                      },
               LOGGER_NAME : {'level' : 'INFO',
                            'handlers' : ['consoleHandler',],
                            'qualname' : LOGGER_NAME
                            }
               },
   }

userDir = os.path.expanduser("~")
logConfigFile = os.path.join(userDir, LOGGER_NAME + 'Log.config')
if os.path.exists(logConfigFile):
    print ("logConfigFile " + logConfigFile )
    try:
        logging.config.fileConfig(logConfigFile, 
                                  disable_existing_loggers=False )
        print("Success Openning logfile")
    except (NoSectionError,TypeError) as ex:
        print ("In Exception to load dictConfig package %s Because of "
               "exeption\n  %s" % (LOGGER_NAME, ex))
        logging.config.dictConfig(LOGGER_DEFAULT)
    except KeyError as ex:
        print ("logfile %s was missing or had errant sections %s" %
               (logConfigFile, ex.args))
else:
    logging.config.dictConfig(LOGGER_DEFAULT)
logger = logging.getLogger(LOGGER_NAME)
        

print("__name__: %s" %__name__)
 
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
class DepositionListDevice(Device):
    '''
    Generic device type for our project
    '''
    def __init__(self, *args, instance_number=0, config_file="", **kwargs):
        self.prefix = args[0]
        self.instance_number=instance_number
        self.instance_letter=chr(instance_number+64)
        #print ("kwargs %s" % kwargs)
        super(DepositionListDevice, self).__init__(*args, **kwargs)
        
                
            
    def loadListFile(self):
        configuration = {}
        with open(self.config_file, 'r') as config:
            config_reader = csv.DictReader(config)
            numAttr = 0
            for row in config_reader:
                if row['object'] == self.__class__.__name__:
                    configuration[numAttr] = row
                    numAttr += 1
        logger.debug ("\nconfiguration %s\n" % configuration)

        return configuration
        
class ChamberCryoPump(DepositionListDevice):
    cryo_power_on = FC(EpicsSignal, 
                       '{self.prefix}{self.cryo_on_read_pv_suffix}',
               write_pv='{self.prefix}{self.cryo_on_write_pv_suffix}',
               name = 'cryo_power_on')
    cryo_exhaust_to_vp1 = FC(EpicsSignal, 
                             '{self.prefix}{self.cryo_exhaust_read_pv_suffix}',
                           write_pv='{self.prefix}{self.cryo_exhaust_write_pv_suffix}',
                           name = 'cryo_exhaust_to_vp1')
    cryo_pressure = FC(EpicsSignal, "{self.prefix}{self.cryo_pressure_read_pv_suffix}",
                    name = 'cryo_pressure')
    cryo_temperature_status = FC(EpicsSignal, 
                                 "{self.prefix}{self.cryo_temp_status_read_pv_suffix}",
                            name= 'cryo_temperature_status')    
    def __init__(self, prefix, 
                 cryo_on_read_pv_suffix,
                 cryo_on_write_pv_suffix,
                 cryo_exhaust_read_pv_suffix,
                 cryo_exhaust_write_pv_suffix,
                 cryo_pressure_read_pv_suffix,
                 cryo_temp_status_read_pv_suffix, **kwargs):
        self.cryo_on_read_pv_suffix = cryo_on_read_pv_suffix
        self.cryo_on_write_pv_suffix = cryo_on_write_pv_suffix
        self.cryo_exhaust_read_pv_suffix = cryo_exhaust_read_pv_suffix
        self.cryo_exhaust_write_pv_suffix = cryo_exhaust_write_pv_suffix
        self.cryo_pressure_read_pv_suffix = cryo_on_read_pv_suffix
        self.cryo_temp_status_read_pv_suffix = cryo_temp_status_read_pv_suffix
        super(ChamberCryoPump, self).__init__(prefix, **kwargs)
        
    def is_cryo_on(self):
        return self.cryo_power_on.get() == 1
        
    def is_cryo_exhausting_to_vp1(self):
        return self.cryo_exhaust_to_vp1.get() == 1
    
    def set(self):
        '''
        Turn the cryo pump on, but make sure that it is ready before turning it
        on and make sure that it is on before completion
        '''
class GateValve(DepositionListDevice):
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_1_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_1_Pos_OUT",
                             tolerance=0.5,
                             name='gate_valve_position')
    gate_valve_close_request = FC(EpicsSignal, \
                      "{self.prefix}:plc:Landing_Chamber_Cryo_GV1_CLOSED_RB", \
                          write_pv="{self.prefix}:plc:LC_Cryo_GV1_Close_OUT", \
                          name = 'gate_valve_close_request')
    gate_valve_open_request = FC(EpicsSignal, \
                         "{self.prefix}:plc:Landing_Chamber_Cryo_GV1_OPEN_RB", \
                         write_pv="{self.prefix}:plc:LC_Cryo_GV1_Open_OUT", \
                         name='gate_valve_open_request')
    gate_valve_fully_closed = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LC_GV1_DoorClosed_IN', \
                                 name = 'gate_valve_fully_closed')
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LC_GV1_DoorOpen_IN', \
                                 name = 'gate_valve_fully_open')
    
    
class ChamberWithGateValve(Device):
    VALVE_ALL_OPEN = 100.0
    VALVE_ALL_CLOSED = 0.000
    gate_valve_position = None
    gate_valve_close_request = None
    gate_valve_open_request = None
    gate_valve_fully_open = None
    gate_valve_fully_closed = None
     
    def __init__(self):
        super(ChamberWithGateValve, self).__init__(*args, **kwargs)
     
    def close_gate_valve(self, group='gate_valves'):
        logger.info("Closing gate valve")
        yield from bps.abs_set(self.gate_valve_position, \
                               VALVE_ALL_CLOSED,\
                               group=group)
         
    def open_gate_valve(self, position=VALVE_ALL_OPEN, \
                        group='gate_valves'):
        logger.info("Opening gate valve to position %f" % position )
        yield from bps.abs_set(self.gate_valve_position, \
                               position, \
                               group=group)
         
class ChamberWithColdCathodeGage(Device):
    ENABLE_TEXT = 'Enable'
    DISABLE_TEXT = 'Disable'
    ccg_power_on = None
    ccg_pressure = None
 
    def __init__(self):
        super(ChamberWithColdCathodeGage, self).__init__(*args, **kwargs)
     
    def disable_ccg(self, group='cathode_gauges'):
        logging.info("Disabling CCG")
        yield from abs_set(ccg_power_on, self.DISABLE_TEXT, group=group)
         
    def enable_ccg(self, group='cathode_gauges'):
        logging.info("Disabling CCG")
        yield from abs_set(ccg_power_on, self.DISABLE_TEXT, group=group)
         

    
class LandingChamber(DepositionListDevice):
    '''
    Device to describe the landing chamber
    '''
#     cryo_power_on = FC(EpicsSignal, 
#                        "{self.prefix}:plc:CP1_Landing_Chamber_Cryo_Pump_RB",
#                write_pv='{self.prefix}:plc:CP1_LC_Cryo_Pump_Off_OUT',
#                name = 'cryo_power_on')DDC
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, 
#                              '{self.prefix}:plc:CP1_Exhaust_to_VP1_RB',
#                            write_pv='{self.prefix}:plc:CP1_Exhaust_VP1_On_OUT',cryo_temp_status_read_pv_suffix
#                            name = 'cryo_exhaust_to_vp1')
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_5_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, 
#                                  "{self.prefix}:plc:Cryo_Pump_1_ok_IN",
#                             name= 'cryo_temperature_status')
#     cryo_power_on = FC(EpicsSignal, 
#                        '{self.prefix}{cryo_on_read_pv_suffix}',
#                write_pv='{self.prefix}{cryo_on_write_pv_suffix}',
#                name = 'cryo_power_on')
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, 
#                              '{self.prefix}{cryo_exhaust_read_pv_suffix}',
#                            write_pv='{self.prefix}{cryo_exhaust_write_pv_suffix}',
#                            name = 'cryo_exhaust_to_vp1')
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}{cryo_pressure_read_pv_suffix}",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, 
#                                  "{self.prefix}{cryo_temp_read_pv_suffix}",
#                             name= 'cryo_temperature_status')    
    cryo_config = OrderedDict()
    cryo_config['cryo_pump'] = (ChamberCryoPump, '',
                                {'cryo_on_read_pv_suffix': ':plc:CP1_Landing_Chamber_Cryo_Pump_RB',
                                 'cryo_on_write_pv_suffix': ':plc:CP1_LC_Cryo_Pump_Off_OUT',
                                 'cryo_exhaust_read_pv_suffix': ':plc:CP1_Exhaust_to_VP1_RB',
                                 'cryo_exhaust_write_pv_suffix':':plc:CP1_Exhaust_VP1_On_OUT',
                                 'cryo_pressure_read_pv_suffix': ':plc:Cryo_Pump_1_ok_IN',
                                 'cryo_temp_status_read_pv_suffix': ':plc:Cryo_Pump_1_ok_IN',
                                 'kind': Kind.normal})
    print("Cryo_config %s" % cryo_config)
    cryo_pump = DDC(cryo_config)
#     cryo_power_on = FC(EpicsSignal, 
#                        "{self.prefix}:plc:CP1_Landing_Chamber_Cryo_Pump_RB",
#                write_pv='{self.prefix}:plc:CP1_LC_Cryo_Pump_Off_OUT',
#                name = 'cryo_power_on')
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, 
#                              '{self.prefix}:plc:CP1_Exhaust_to_VP1_RB',#     cryo_power_on = FC(EpicsSignal, 
#                        "{self.prefix}:plc:CP1_Landing_Chamber_Cryo_Pump_RB",
#                write_pv='{self.prefix}:plc:CP1_LC_Cryo_Pump_Off_OUT',
#                name = 'cryo_power_on')
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, 
#                              '{self.prefix}:plc:CP1_Exhaust_to_VP1_RB',
#                            write_pv='{self.prefix}:plc:CP1_Exhaust_VP1_On_OUT',
#                            name = 'cryo_exhaust_to_vp1')
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_5_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, 
#                                  "{self.prefix}:plc:Cryo_Pump_1_ok_IN",
#                             name= 'cryo_temperature_status')
#                            write_pv='{self.prefix}:plc:CP1_Exhaust_VP1_On_OUT',
#                            name = 'cryo_exhaust_to_vp1')
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_5_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, 
#                                  "{self.prefix}:plc:Cryo_Pump_1_ok_IN",
#                             name= 'cryo_temperature_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP1_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP1_OUT",
                  name = 'n2_purge',
                  string=True)
    ccg_power_on = FC(EpicsSignal, "{self.prefix}:plc:Landing_Chamber_CCG1_RB",
                  write_pv = "{self.prefix}:plc:LC_CCG1_Enable_OUT",
                  name = 'ccg_power_on',
                  put_complete=True,
                  string=True)
    ccg_pressure = FC(EpicsSignal,
                      '{self.prefix}:plc:CCG_1_IN',
                      name='ccg_pressure')
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_1_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_1_Pos_OUT",
                             tolerance=0.5,
                             name='gate_valve_position')
    gate_valve_close_request = FC(EpicsSignal, \
                      "{self.prefix}:plc:Landing_Chamber_Cryo_GV1_CLOSED_RB", \
                          write_pv="{self.prefix}:plc:LC_Cryo_GV1_Close_OUT", \
                          name = 'gate_valve_close_request')
    gate_valve_open_request = FC(EpicsSignal, \
                         "{self.prefix}:plc:Landing_Chamber_Cryo_GV1_OPEN_RB", \
                         write_pv="{self.prefix}:plc:LC_Cryo_GV1_Open_OUT", \
                         name='gate_valve_open_request')
    gate_valve_fully_closed = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LC_GV1_DoorClosed_IN', \
                                 name = 'gate_valve_fully_closed')
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LC_GV1_DoorOpen_IN', \
                                 name = 'gate_valve_fully_open')

    def disable_ccg(self, group='cathode_gauges'):
        logging.info("Disabling CCG")#     cryo_power_on = FC(EpicsSignal, 
#                        "{self.prefix}:plc:CP1_Landing_Chamber_Cryo_Pump_RB",
#                write_pv='{self.prefix}:plc:CP1_LC_Cryo_Pump_Off_OUT',
#                name = 'cryo_power_on')
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, 
#                              '{self.prefix}:plc:CP1_Exhaust_to_VP1_RB',
#                            write_pv='{self.prefix}:plc:CP1_Exhaust_VP1_On_OUT',
#                            name = 'cryo_exhaust_to_vp1')
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_5_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, 
#                                  "{self.prefix}:plc:Cryo_Pump_1_ok_IN",
#                             name= 'cryo_temperature_status')
        yield from bps.abs_set(self.ccg_power_on, CCG_OFF_VALUE, \
                               group=group)
        
    def enable_ccg(self, group='cathode_gauges'):
        logging.info("Disabling CCG")
        yield from bps.abs_set(self.ccg_power_on, CCG_ON_VALUE, \
                               group=group)
       
    def close_gate_valve(self, group='gate_valves'):
        logger.info("Closing gate valve")
        yield from bps.abs_set(self.gate_valve_position, \
                               VALVE_ALL_CLOSED,\
                               group=group)
        
    def open_gate_valve(self, position=100.0, \
                        group='gate_valves'):
        logger.info("Opening gate valve to position %f" % position )
        yield from bps.abs_set(self.gate_valve_position, \
                               position, \
                               group=group)

    
class PlanarChamber(DepositionListDevice):
    '''
    Device to describe the Planar chamber
    '''
    cryo_config = OrderedDict()
    cryo_config['cryo_pump'] = (ChamberCryoPump, '',
                                {'cryo_on_read_pv_suffix': ':plc:CP2_Planar_Chamber_Cryo_Pump_RB',
                                 'cryo_on_write_pv_suffix': ':plc:CP2_PC_Cryo_Pump_Off_OUT',
                                 'cryo_exhaust_read_pv_suffix': ':plc:CP2_Exhaust_to_VP1_RB',
                                 'cryo_exhaust_write_pv_suffix':':plc:CP2_Exhaust_VP1_On_OUT',
                                 'cryo_pressure_read_pv_suffix': ':plc:Cryo_Pump_2_ok_IN',
                                 'cryo_temp_status_read_pv_suffix': ':plc:Cryo_Pump_2_ok_IN',
                                 'kind': Kind.normal})
    print("Cryo_config %s" % cryo_config)
    cryo_pump = DDC(cryo_config)
#     cryo_power_on = FC(EpicsSignal,
#                          '{self.prefix}:plc:CP2_Planar_Chamber_Cryo_Pump_RB',
#                          write_pv='{self.prefix}:plc:CP2_PC_Cryo_Pump_Off_OUT',
#                          name='cryo_power_on',
#                          string=True)
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_6_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, \
#                                  "{self.prefix}:plc:Cryo_Pump_2_ok_IN",
#                                  string=True,
#                                  name='cryo_temp_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP2_RB",
                            write_pv="{self.prefix}:plc:N2_Purge_CP2_OUT",
                            name = 'n2_purge',
                            string=True)
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_2_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_2_Pos_OUT",
                             tolerance=0.5,
                             name='gate_valve_position')#     cryo_power_on = FC(EpicsSignal,
#                          '{self.prefix}:plc:CP4_Loadlock_Chamber_Cryo_Pump_RB',
#                          write_pv='{self.prefix}:plc:CP4_LLC_Cryo_Pump_Off_OUT',
#                          name='cryo_power_on',
#                          string=True)
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_8_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, "{self.prefix}:plc:Cryo_Pump_4_ok_IN",
#                              string=True,
#                              name='cryo_temperature_status')
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, \
#                          '{self.prefix}:plc:CP4_Exhaust_to_VP1_RB',
#                          write_pv='{self.prefix}:plc:CP4_Exhaust_VP1_On_OUT',
#                          name='cryo_exhaust_to_vp1',
#                          string=True
#                             )
    gate_valve_close_request = FC(EpicsSignal, \
                      "{self.prefix}:plc:Planar_Chamber_Cryo_GV2_CLOSED_RB", \
                      write_pv="{self.prefix}:plc:LC_Cryo_GV2_Close_OUT", \
                      name = 'gate_valve_close_request', \
                      string='True')
    gate_valve_open_request = FC(EpicsSignal, \
                     "{self.prefix}:plc:Planar_Chamber_Cryo_GV2_OPEN_RB", \
                     write_pv="{self.prefix}:plc:LC_Cryo_GV2_Open_OUT", \
                     name='gate_valve_open_request', \
                     string=True)
    gate_valve_fully_closed = FC(EpicsSignal, \
                     '{self.prefix}:plc:RC_GV2_Closed_IN', \
                     name = 'gate_valve_fully_closed',
                     string=True)
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:RC_GV2_Open_IN', \
                                 name = 'gate_valve_fully_open', \
                                 string=True)
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, \
#                          '{self.prefix}:plc:CP2_Exhaust_to_VP1_RB',
#                          write_pv='{self.prefix}:plc:CP2_Exhaust_VP1_On_OUT',
#                          name='cryo_exhaust_to_vp1',
#                          string=True
#                             )
    def close_gate_valve(self, group='gate_valves'):
        logger.info("Closing gate valve")
        yield from bps.abs_set(self.gate_valve_position, \
                               VALVE_ALL_CLOSED,\
                               group=group)
        
    def open_gate_valve(self, position=VALVE_ALL_OPEN, \
                        group='gate_valves'):
        logger.info("Opening gate valve to position %f" % position )
        yield from bps.abs_set(self.gate_valve_position, \
                               position, \
                               group=group)
            
class RoundChamber(DepositionListDevice):
    '''
    Device to describ the Round Chamber
    '''
    cryo_config = OrderedDict()
    cryo_config['cryo_pump'] = (ChamberCryoPump, '',
                                {'cryo_on_read_pv_suffix': ':plc:CP3_Round_Chamber_Cryo_Pump_RB',
                                 'cryo_on_write_pv_suffix': ':plc:CP3_RC_Cryo_Pump_Off_OUT',
                                 'cryo_exhaust_read_pv_suffix': ':plc:CP3_Exhaust_to_VP1_RB',
                                 'cryo_exhaust_write_pv_suffix':':plc:CP3_Exhaust_VP1_On_OUT',
                                 'cryo_pressure_read_pv_suffix': ':plc:Cryo_Pump_3_ok_IN',
                                 'cryo_temp_status_read_pv_suffix': ':plc:Cryo_Pump_3_ok_IN',
                                 'kind': Kind.normal})
    print("Cryo_config %s" % cryo_config)
    cryo_pump = DDC(cryo_config)
#     cryo_power_on = FC(EpicsSignal,
#                          '{self.prefix}:plc:CP3_Round_Chamber_Cryo_Pump_RB',
#                          write_pv='{self.prefix}:plc:CP3_RC_Cryo_Pump_Off_OUT',
#                          name='cryo_power_on',
#                          string=True)
#     cp_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_7_IN",
#                     name = 'cp3_pressure')
#     cryo_temperature_status = FC(EpicsSignal, \
#                                  "{self.prefix}:plc:Cryo_Pump_3_ok_IN", 
#                                  string=True,
#                                  name='cryo_temperature_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP3_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP3_OUT",
                  name = 'n2_purge',
                  string=True)
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_3_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_3_Pos_OUT",
                             tolerance=0.5,
                             name='gate_valve_position')
    gate_valve_close_request = FC(EpicsSignal, \
                      "{self.prefix}:plc:Round_Chamber_Cryo_GV3_CLOSED_RB", \
                      write_pv="{self.prefix}:plc:LC_Cryo_GV3_Close_OUT", \
                      name = 'gate_valve_close_request', \
                      string='True')
    gate_valve_open_request = FC(EpicsSignal, \
                         "{self.prefix}:plc:Round_Chamber_Cryo_GV3_OPEN_RB", \
                         write_pv="{self.prefix}:plc:LC_Cryo_GV3_Open_OUT", \
                         name='gate_valve_open_request', \
                         string=True)
    gate_valve_fully_closed = FC(EpicsSignal, \
                                 '{self.prefix}:plc:PC_GV3_Closed_IN', \
                                 name = 'gate_valve_fully_closed', \
                                 string=True)
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:PC_GV3_Open_IN', \
                                 name = 'gate_valve_fully_open', \
                                 string=True)
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, \
#                          '{self.prefix}:plc:CP3_Exhaust_to_VP1_RB',
#                          write_pv='{self.prefix}:plc:CP3_Exhaust_VP1_On_OUT',
#                          name='cryo_exhaust_to_vp1',
#                          string=True
#                             )
    
    def close_gate_valve(self, group='gate_valves'):
        '''
        Convenient method to close the gate valve
        '''
        logger.info("Closing gate valve")
        yield from bps.abs_set(self.gate_valve_position, \
                               VALVE_ALL_CLOSED,\
                               group=group)
        
    def open_gate_valve(self, position=VALVE_ALL_OPEN, \
                        group='gate_valves'):
        '''
        Convenient method to open the gate valve
        '''
        logger.info("Opening gate valve to position %f" % position )
        yield from bps.abs_set(self.gate_valve_position, \
                               position, \
                               group=group)

class LoadlockChamber(DepositionListDevice):
    '''
    Device to describe the Load Lock chamber
    '''
    cryo_config = OrderedDict()
    cryo_config['cryo_pump'] = (ChamberCryoPump, '',
                                {'cryo_on_read_pv_suffix': ':plc:CP4_Loadlock_Chamber_Cryo_Pump_RB',
                                 'cryo_on_write_pv_suffix': ':plc:CP4_LLC_Cryo_Pump_Off_OUT',
                                 'cryo_exhaust_read_pv_suffix': ':plc:CP4_Exhaust_to_VP1_RB',
                                 'cryo_exhaust_write_pv_suffix':':plc:CP4_Exhaust_VP1_On_OUT',
                                 'cryo_pressure_read_pv_suffix': ':plc:Cryo_Pump_4_ok_IN',
                                 'cryo_temp_status_read_pv_suffix': ':plc:Cryo_Pump_4_ok_IN',
                                 'kind': Kind.normal})
    print("Cryo_config %s" % cryo_config)
    cryo_pump = DDC(cryo_config)
#     cryo_power_on = FC(EpicsSignal,
#                          '{self.prefix}:plc:CP4_Loadlock_Chamber_Cryo_Pump_RB',
#                          write_pv='{self.prefix}:plc:CP4_LLC_Cryo_Pump_Off_OUT',
#                          name='cryo_power_on',
#                          string=True)
#     cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_8_IN",
#                     name = 'cryo_pressure')
#     cryo_temperature_status = FC(EpicsSignal, "{self.prefix}:plc:Cryo_Pump_4_ok_IN",
#                              string=True,
#                              name='cryo_temperature_status')
#     cryo_exhaust_to_vp1 = FC(EpicsSignal, \
#                          '{self.prefix}:plc:CP4_Exhaust_to_VP1_RB',
#                          write_pv='{self.prefix}:plc:CP4_Exhaust_VP1_On_OUT',
#                          name='cryo_exhaust_to_vp1',
#                          string=True
#                             )
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP4_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP4_OUT",
                  name = 'n2_purge',
                  string=True)
    ccg_power_on = FC(EpicsSignal, "{self.prefix}:plc:Loadlock_CCG2_RB",
                   write_pv = "{self.prefix}:plc:LL_CCG2_Enable_OUT",
                 name='power_on',
                 put_complete=True,
                   string=True)
    ccg_pressure = FC(EpicsSignal,
                      '{self.prefix}:plc:CCG_2_IN')

    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_4_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_4_Pos_OUT",
                             tolerance=0.5,
                             name='gate_valve_position')
    gate_valve_close_request = FC(EpicsSignal, \
                      "{self.prefix}:plc:Loadlock_Chamber_Cryo_GV4_CLOSED_RB", \
                      write_pv="{self.prefix}:plc:LC_Cryo_GV4_Close_OUT", \
                      name = 'gate_valve_close_request', \
                      string='True')
    gate_valve_open_request = FC(EpicsSignal, \
                     "{self.prefix}:plc:Loadlock_Chamber_Cryo_GV4_OPEN_RB", \
                     write_pv="{self.prefix}:plc:LC_Cryo_GV4_Open_OUT", \
                     name='gate_valve_open_request', \
                     string=True)# class ChamberWithGateValve(Device):

    gate_valve_fully_closed = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LL_GV4_Closed_IN', \
                                 name = 'gate_valve_fully_closed', \
                                 string=True)
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LL_GV4_Open_IN', \
                                 name = 'gate_valve_fully_open', \
                                 string=True)
    ar_backfill_high_rate = FC(EpicsSignal,
                   '{self.prefix}:plc:EOV3_Process_Argon_Hi_Backfill_RB',
                   write_pv='{self.prefix}:plc:LL_Ar_Hi_Bf_On_OUT',
                   name='ar_backfill_high_# class ChamberWithGateValve(Device):rate',
                   string=True)
    ar_backfill_low_rate = FC(EpicsSignal,
                  '{self.prefix}:plc:Ar_Backfill_to_LL_RB',
                  write_pv='{self.prefix}:plc:Ar_Backfill_LL_On_OUT',
                  name='ar_backfill_low_rate',
                  string=True)                   

    def close_gate_valve(self, group='gate_valves'):
        '''
        Convenient method to close the chamber'gate valve
        '''
        logger.info("Closing gate valve")
        yield from bps.abs_set(self.gate_valve_position, \
                               VALVE_ALL_CLOSED,\
                               group=group)
        
    def open_gate_valve(self, position=VALVE_ALL_OPEN, \
                        group='gate_valves'):
        '''
        Convenient method to open the chamber's gate valve.  By default, it will 
        open fully
        '''
        logger.info("Opening gate valve to position %f" % position )
        yield from bps.abs_set(self.gate_valve_position, \
                               position, \
                               group=group)

    def disable_ccg(self, group='cathode_gauges'):
        '''
        Method to disable the CCG.  Too much air in the system too quickly is
        bad for the gauge head
        '''
        logging.info("Disabling CCG")
        yield from bps.abs_set(self.ccg_power_on, \
                               CCG_OFF_VALUE, \
                               group=group)
        
    def enable_ccg(self, group='cathode_gauges'):
        '''
        Method to enable the cold cathode gauge.  
        '''
        logging.info("Disabling CCG")
        yield from bps.abs_set(self.ccg_power_on, \
                               CCG_ON_VALUE, \
                               group=group)

class CenterChamber(DepositionListDevice):
    '''
    Device to describe the center chamber
    '''
    
    exhaust_to_vp1 = FC(EpicsSignal,
                        '{self.prefix}:plc:CC_Exhaust_to_VP1_RB',
                        write_pv='{self.prefix}:plc:CC_Exhaust_VP1_On_OUT',
                        name = 'exhaust_to_vp1',
                        string='True'
                        )
    overpressure = FC(EpicsSignal,
                      '{self.prefix}:plc:Center_Chamber_Overpressure_RB',
                      write_pv='{self.prefix}:plc:CC_OverPress_Close_OUT',
                      name='overpressure',
                      string=True) 
    ar_backfill_high_rate = FC(EpicsSignal,
                       '{self.prefix}:plc:EOV2_Loadlock_Argon_Hi_Backfill_RB',
                       write_pv='{self.prefix}:plc:Process_Ar_Hi_Bf_On_OUT',
                       name='ar_backfill_high_rate',
                       string=True)
    ar_backfill_low_rate = FC(EpicsSignal,
                      '{self.prefix}:plc:Ar_Backfill_to_Center_RB',
                      write_pv='{self.prefix}:plc:Ar_Backfill_CC_On_OUT',
                      name='ar_backfill_low_rate',
                      string=True)
    
        

class MassFlowControl(DepositionListDevice):
    '''
    Device to describe a mass flow controller
    '''
    PURGE_TEXT = 'purge'
    LOW_LEVEL_VALUE_TEXT = 'low_level_value'
    LOW_LEVEL_DEFAULT_VALUE = 5.0
    VALVE_CLOSED_VALUE=0
    VALVE_OPEN_VALUE=1
    EPICS_PID_CONTROL_DISABLE=0
    EPICS_PID_CONTROL_ENABLE=1
    PLC_BYPASS_DISABLE=0
    PLC_BYPASS_ENABLE=1
    flow = FC(EpicsSignal, "{self.prefix}:plc:MFC_{self.instance_number}_IN",
               write_pv="{self.prefix}:plc:MFC_{self.instance_number}_OUT", 
                          kind=Kind.config,
                          put_complete=True)
    valve_on = FC(EpicsSignal, \
          "{self.prefix}:plc:MFC{self.instance_number}_RB",
          write_pv = "{self.prefix}:plc:MFC{self.instance_number}_RC_On_OUT", 
          kind=Kind.config,
          put_complete=True,
          string=True)
    plc_bypass = FC(EpicsSignal, \
            "{self.prefix}:plc:MFC{self.instance_number}_Manual_OUT",
            write_pv = "{self.prefix}:plc:MFC{self.instance_number}_Manual_OUT", 
            put_complete=True,
            kind=Kind.config, 
            string=True)
    epics_pid_control = FC(EpicsSignal, \
               '{self.prefix}:userCalc1.{self.instance_letter}',
                write_pv = '{self.prefix}:userCalc1.{self.instance_letter}' , 
                kind=Kind.config,
                put_complete=True,
                string=True)
    
    def __init__(self, *args, ch_name=None, mixerNumber=0, mixtureID="", \
                 flow=0, **kwargs):
        self.chName = ch_name
        self.mixtureID = mixtureID
        super(MassFlowControl, self).__init__(*args, **kwargs)
        #depos_sys.gun_selector.ps1_voltage
        
    def close_valve(self, group=None, wait=False):
        '''
        Close the valve that lets deposition gas into the system
        '''
        logging.info("closing valve mfc%d" % self.instance_number)
        yield from bps.abs_set(self.valve_on, self.VALVE_CLOSED_VALUE, \
                               group=group, wait=wait)
        
    def disable_epics_pid_control(self, group=None, wait=False):
        '''
        Disable EPICS PID control
        '''
        logging.info("disabling epics_pid_control mfc%d" % self.instance_number)
        yield from bps.abs_set(self.epics_pid_control, \
                               self.EPICS_PID_CONTROL_DISABLE, \
                               group=group, wait=wait)
        
    def disable_plc_bypass(self, group=None, wait=False):
        '''Disable the PLC bypass
        '''
        logger.info("disabling_plc_bypass mfc%d" % self.instance_number)
        yield from bps.abs_set(self.plc_bypass, \
                               self.PLC_BYPASS_DISABLE, \
                               group=group, wait=wait)
        
    def enable_epics_pid_control(self, group=None, wait=False):
        '''
        Enable EPICS PID control
        '''
        logger.info("enabling_epics_pid_control mfc%d" % self.instance_number)
        yield from bps.abs_set(self.epics_pid_control, \
                               self.EPICS_PID_CONTROL_ENABLE, \
                               group=group, wait=wait)
        
    def enable_plc_bypass(self, group=None, wait=False):
        '''
        Enable the PLC bypass
        '''
        logger.info("enabling pcl_bypass mfc%d" %self.instance_number)
        yield from bps.abs_set(self.plc_bypass, \
                               self.PLC_BYPASS_ENABLE, group=group, wait=wait)
        
    def open_valve(self, group=None, wait=False):
        '''
        Open the valve letting in Deposition gasses
        '''
        logger.info("enabling valve mfc%d" % self.instance_number)
        yield from bps.abs_set(self.valve_on, self.VALVE_OPEN_VALUE, \
                               group=group, wait=wait)
        
#     def set_flow(self, new_flow, group=None, wait=False):
#         logger.info("setting mfc%d flow to %f" %(self.instance, new_flow))
#         yield from bps.abs_set(self.flow, new_flow, group=group, wait=wait)
        
    def purge(self, leak_rate, low_check_value, group=None, wait=False):
        '''
        Purge the syestem.  This method should probably go away.  It is
        intended to be replaved by the purge option on the "set" command
        '''
        logger.info("preparing to purging mfc %d")
        done_status = DeviceStatus(self)
        self.valve_on.set(self.VALVE_OPEN_VALUE)
        self.plc_bypass.set(self.PLC_BYPASS_ENABLE)
        self.epics_pid_control(self.EPICS_PID_CONTROL_DISABLE)
        self.flow.set(leak_rate)
        def purge_done_cb(value, timestamp, **kwargs):
            if value < low_check_value:
                logger.info("purge of mfc%d is completed" %self.instance_number)
                self.valve_on.set(self.VALVE_CLOSED_VALUE)
                self.flow.clear_sub(purge_done_cb)
                done_status._finished()
        self.flow.subscribe(purge_done_cb)
        return done_status
    
    def set(self, flow_rate, **kwargs):
        '''
        sets the flow of the mass flow controller.  kwargs may contain 
        "purge" a boolean
        "low_level_value" - a float value
        if purge is true, then this will wait until the value of flow is less 
        than the low check value.  Once below the level, this returns a finished
        status.
        If purge is false, then it immediately returns a finished status.
        '''
        logger.info("preparing to set flow mfc %f" % flow_rate)
        done_status = DeviceStatus(self, settle_time=30.0)
        start_time = time.time()
        
        if self.PURGE_TEXT in kwargs:
            purge = kwargs[self.PURGE_TEXT]
            #del kwargs[self.PURGE_TEXT]
        else:
            purge = False
        if purge == True:
            logger.info('doing a purging set')
            self.valve_on.set(self.VALVE_OPEN_VALUE)
            self.plc_bypass.set(self.PLC_BYPASS_ENABLE)
            self.epics_pid_control.set(self.EPICS_PID_CONTROL_DISABLE)
            set_stat = self.flow.set(flow_rate)
            status_wait(set_stat, 30)
            if self.LOW_LEVEL_VALUE_TEXT in kwargs:
                low_level_value = kwargs[self.LOW_LEVEL_VALUE_TEXT]
                #del kwargs[self.LOW_LEVEL_VALUE_TEXT]
            else:
                low_level_value = self.LOW_LEVEL_DEFAULT_VALUE
            def purge_done_cb(value, timestamp, **kwargs):
                time_now = time.time()
                time_since_set = time_now-start_time
                if value < low_level_value:
                    logger.info("purge of mfc%d is completed" %self.instance_number)
                    self.flow.set(0.0)
                    self.valve_on.set(self.VALVE_CLOSED_VALUE)
                    self.flow.clear_sub(purge_done_cb) 
                    done_status._finished()
            self.flow.subscribe(purge_done_cb)
        else:
            logger.info('doing a normal set')
            self.flow.set(flow_rate)
            done_status._finished()
        return done_status
    
    def shutdown(self):
        '''
        prepare for shutdown after use
        '''
        yield from self.disable_epics_pid_control()
        yield from self.set_flow(0.0)
        yield from self.close_valve()
            

def _mfc_fields( prefix, field_base, range_, **kwargs):
    defn = OrderedDict()
    
    for i in range_:
        suffix = '{field}{i}'.format(field=field_base, i=i)
        #kwargs['instance_number'] = i
        #kwargs['instance_letter'] = chr(i+64)
        defn['{}{}'.format(field_base, i)] = \
            (MassFlowControl, prefix, {'instance_number':i, 'kind':Kind.normal})
    return defn

class GasMixer(DepositionListDevice):
    MIXED_RELAY_NAME_PATTERN = 'gm_relay_%dm'
    ARGON_RELAY_NAME_PATTERN = 'gm_relay_%da'
    RELAY_OPEN_TEXT = 'High'
    RELAY_CLOSE_TEXT = 'Low'
    gm_mfc_1_flow = FC(EpicsSignal, "{self.prefix}:LJT7:1:AI0",
                       write_pv="{self.prefix}:LJT7:1:AO2",
                       name='gm_mfc_1_flow')
    gm_mfc_2_flow = FC(EpicsSignal, "{self.prefix}:LJT7:1:AI2",
                       write_pv="{self.prefix}:LJT7:1:AI7",
                       name='gm_mfc_2_flow')
    gm_mfc_3_flow = FC(EpicsSignal, "{self.prefix}:LJT7:1:AI3",
                       write_pv="{self.prefix}:LJT7:1:AI8",
                       name='gm_mfc_3_flow')
    gm_mfc_1_purge = FC(EpicsSignal, "{self.prefix}:LJT7:1:DO0",
                     string=True)
    gm_mfc_2_purge = FC(EpicsSignal, "{self.prefix}:LJT7:1:DO1",
                     string=True)
    gm_pid2_fb_on = FC(EpicsSignal, "{self.prefix}:async_pid_slow2.FBON",
                       name = "gm_pid2_fb_on",
                       string=True)
    gm_pid2_setpoint = FC(EpicsSignal, "{self.prefix}:async_pid_slow2.VAL",
                          name = 'gm_pid2_setpoint')
    gm_pid3_fb_on = FC(EpicsSignal, "{self.prefix}:async_pid_slow3.FBON",
                       name = "gm_pid3_fb_on",
                       string=True)
    gm_pid3_setpoint = FC(EpicsSignal, "{self.prefix}:async_pid_slow3.VAL",
                          name = 'gm_pid3_setpoint')
    gm_mfc_3_purge = FC(EpicsSignal, "{self.prefix}:LJT7:1:DO8",
                     string=True)
    gm_relay_1a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO0",
                     name = 'gm_relay_1a',
                     string=True)
    gm_relay_1m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO1",
                     name = 'gm_relay_1m',
                     string=True)
    gm_relay_2a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO2",
                     name = 'gm_relay_2a',
                     string=True)
    gm_relay_2m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO3",
                     name = 'gm_relay_2m',
                     string=True)
    gm_relay_3a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO4",
                     name = 'gm_relay_3a',
                     string=True)
    gm_relay_3m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO5",
                     name = 'gm_relay_3m',
                     string=True)
    gm_relay_4a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO6",
                     name = 'gm_relay_4a',
                     string=True)
    gm_relay_4m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO7",
                     name = 'gm_relay_4m',
                     string=True)
    gm_relay_5a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO8",
                     name = 'gm_relay_5a',
                     string=True)
    gm_relay_5m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO9",
                     name = 'gm_relay_5m',
                     string=True)
    gm_relay_6a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO10",
                     name = 'gm_relay_6a',
                     string=True)
    gm_relay_6m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO11",
                     name = 'gm_relay_6m',
                     string=True)
    gm_relay_7a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO12",
                     name = 'gm_relay_7a',
                     string=True)
    gm_relay_7m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO13",
                     name = 'gm_relay_7m',
                     string=True)
    gm_relay_8a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO14",
                     name = 'gm_relay_8a',
                     string=True)
    gm_relay_8m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO15",
                     name = 'gm_relay_8m',
                     string=True)

    mfcs = DDC(_mfc_fields('', 'mfc',  range(1, 9)))
    
    def close_mfc_valves(self, mfc_names=None):
        '''
        Close the valves which feed deposition gas mixture to the deposition
        chamber
        '''
        logger.info("Closing valves for all MFCs")
        # if mfc_names is empty construct a list of all mfcs
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        # Loop over specified mfcs
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.close_valve(group='close_valves')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='close_valves')
        
    def close_mixed_gas_relays(self, relay_nums=None):
        '''
        Close off mixed gas from entering the chamber
        '''
        #if no valve list is specified then close all the valves.
        if relay_nums is None:
            relay_nums=range(1, 9)
        #loop over closing the selected valves
        for relay in relay_nums:
            relay_name = self.MIXED_RELAY_NAME_PATTERN % relay
            logger.info("closing relay %s" % relay_name)
            yield from bps.abs_set(self.__getattr__(relay_name), \
                                   self.RELAY_CLOSE_TEXT,
                                   group='close_mixed_gas_relays')
        yield from bps.wait(group='close_mixed_gas_relays')
    
    def close_argon_gas_relays(self, relay_nums=None):
        '''
        Close off the pure argon gas supply to the 
        '''
        if relay_nums is None:
            relay_nums=range(1, 9)
        logger.info("relay_nums %s" % relay_nums)
        for relay in relay_nums:
            relay_name = self.ARGON_RELAY_NAME_PATTERN % relay
            logger.info("closing relay %s" % relay_name)
            yield from bps.abs_set(self.__getattr__(relay_name), \
                                   self.RELAY_CLOSE_TEXT, \
                                   group='close_argon_gas_relays')
        yield from bps.wait(group='close_mixed_gas_relays')
    
        
    def disable_mfc_plc_bypass(self, mfc_names=None):
        logger.info("Disabling plc_bypass for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in self.mfcs.component_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.disable_plc_bypass(group='disable_plc_bypass')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='disable_plc_bypass')
        
    def disable_all_gm_pid_loops(self):
        logger.info("disable all gas mixer pid loops")
        yield from mv(self.gm_pid2_setpoint, 0.000)
        yield from mv(self.gm_pid3_setpoint, 0.000)
            
    def disable_mfc_epics_pid_control(self, mfc_names=None):
        logger.info("Disabling epics_pid_control for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
            
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.disable_epics_pid_control(group='disable_pid_control')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='disable_pid_control')
        
    def disable_all_gm_supply_flows(self):
        logger.info("Disabling all gas mixer supply flows")
        yield from bps.mv(self.gm_mfc_1_flow, 0.000)
        yield from bps.mv(self.gm_mfc_2_flow, 0.000)
        yield from bps.mv(self.gm_mfc_2_flow, 0.000)
        
    def enable_mfc_plc_bypass(self, mfc_names=None):
        logger.info("Enabling plc_bypass for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.enable_plc_bypass(group='enable_plc_bypass')
            logger.debug("mfc % s" % mfc )
        bps.wait(group='enable_bps_bypass')
            
    def enable_mfc_epics_pid_control(self, mfc_names=None):
        logger.info("enabling epics_pid_control for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
            
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.enable_epics_pid_control(group='enable_pid_control')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='enable_pid_control')
        
    def open_mixed_gas_relays(self, relay_nums=None):
        #if no relay_nums defined use them all.
        if relay_nums is None:
            relay_nums=range(1, 9)
        # Make sure to close all of the argon gas relays before opening the 
        # mixed gas relays
        yield from self.close_argon_gas_relays()
        #then finally open the mixed gas relayspurge of mfc%d is completed
        for relay in relay_nums:
            relay_name = self.MIXED_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name),
                                   self.RELAY_OPEN_TEXT,
                                   group='open_mixed_gas_relays')
        yield from bps.wait(group='open_mixed_gas_relays')
    
    def open_mfc_valves(self, mfc_names=None):
        logger.info("Opening valves for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.open_valve(group='open_valves')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait('open_valves')
        
    def open_argon_gas_relays(self, relay_nums=None):
        #if no relay numbers are defined than use all of them
        if relay_nums is None:
            relay_nums=range(1, 9)
        # Make sure to close all of the mixed gas relays before openging these
        yield from self.close_mixed_gas_relays()
        # and now open the argon gas relays
        for relay in relay_nums:
            relay_name = self.ARGON_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name),
                                   self.RELAY_OPEN_TEXT,
                               group='open_argon_gas_relays')
        yield from bps.wait(group='open_argon_gas_relays')
    
    def set_mfc_flows(self, new_flow, mfc_names=None):
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from bpbpss.abs_set(mfc, new_flow,group='set_flows')
        yield from bps.wait('set_flows')        

        
    def purge_mfcs(self, mfc_names=None, leak_rate=25, low_value=5):
        
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        self.close_argon_gas_relays()
        self.close_mixed_gas_relays()
        for mfc_name in mfc_names:
            logger.info("Purging %s" % mfc_name)
            mfc = self.mfcs.__getattr__(mfc_name)
#             yield from mfc.open_valve()
#             yield from mfc.enable_plc_bypass()
#             yield from mfc.disable_epics_pid_control()
            kwargs = {'purge': True,
                      'low_check_value':low_value,
                      'group':'purge_mfcs'}
            yield from bps.abs_set(mfc, leak_rate, \
                                   purge=True, low_level_value= low_value, \
                                   depos_group='purge_mfcs')
#             yield from mfc.close_valve()
        bps.sleep(30)
        bps.wait('purge_mfcs')
        

        
    def shutdown(self):
        yield from self.disable_all_supply_flows()
        yield from self.disable_pid_loops()
        yield from self.close_mixed_gas_relays()
        yield from self.close_argon_gas_flows()
        mfc_names = self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_names)
            yield from mfc.shutdown()

        
        
def _gun_fields( prefix, field_base, range_, **kwargs):
    defn = OrderedDict()
    
    for i in range_:
        suffix = '{field}{i}'.format(field=field_base, i=i)
        kwargs['instance_number'] = i
        defn['{}{}'.format(field_base, i)] = (Gun, prefix, \
                                              {'instance_number':i, 
                                               'kind':Kind.normal})
    return defn

class Gun(DepositionListDevice):
    # Configure these as FormattedComponents
    relay_magnetron = FC(EpicsSignal, \
         "{self.prefix}:plc:Magnetron_{self.instance_number}_Power_RB",
          write_pv="{self.prefix}:plc:Mag{self.instance_number}_Pwr_Enable_OUT",
          name="relay_magnetron",
          string=True,
          put_complete=True, 
          kind=Kind.config)
    voltage_avg = FC(EpicsSignal, 
                     "{self.prefix}:userAve{self.instance_number}.VAL",
                      name='voltage_avg', 
                      kind=Kind.config)
    water_flow_cathode_raw = FC(EpicsSignal, \
                            "{self.prefix}w:USB231:1:Ai{self.instance_number}",
                             name='water_flow_cathode_raw', 
                             kind=Kind.config)
    water_flow_cathode = FC(EpicsSignal, \
                        "{self.prefix}:userCalcOut1{self.instance_number}.VAL",
                         name="water_flow_cathode", 
                         kind=Kind.config)
    mask_width = Cpt(Signal, value=40)
    zero_position = Cpt(Signal, value=0.0)
    coat_velocity = Cpt(Signal, value= 75.0)
    travel_velocity = Cpt(Signal, value=75.0)
    high_position = Cpt(Signal, value=0.0)
    low_position = Cpt(Signal, value=0.0)

    def __init__(self, *args, ch_name=None, \
                 mask_width=40.0, zero_position = 1000.0, \
                 sample_lower_extent=100.0, sample_upper_extent = 250, \
                 coat_velocity=10.0, travel_velocity=15.0, \
                 overspray = 45.0, **kwargs):
        self._ch_name = ch_name

#         self.mask_width = mask_width
#         self.zero_position = zero_position
#         self.coat_velocity = coat_velocity
#         self.travel_velocity = travel_velocity
        self.sample_lower_extent = sample_lower_extent
        self.sample_upper_extent = sample_upper_extent
        self.overspray = overspray
        super(Gun, self).__init__(*args, **kwargs)
        self.high_position.put(self.zero_position.value - \
                               self.sample_upper_extent - \
                               self.mask_width.value/self.overspray)
        self.low_position.put(self.zero_position.value - \
                              self.sample_lower_extent - \
                              self.mask_width.value/self.overspray)
        logger.debug("dir(self %s" % dir(self))
        
    def coat_layers(self, motor, number_of_layers):
        logger.info("gun number %d, Motor %s" % (self.instance_number, motor))
        for l in number_of_layers:
            yield from bps.mv(motor.velocity, self.coat_velocity)
            yield from mv(motor, self.high_position)
            yield from bps.sleep(.1)
            yield from bps.mv(motor, self.low_position)

    def home(self, motor, speed=0):
        if speed == 0:
            speed = self.travel_velocity
        logger.info("gun %d, motor, motor: %s, speed" % \
                    (self.instance_number, motor, speed))
        yield from bps.mv(motor.velocity, speed)
        yield from motor.mv(self.zero-position)

    def goToLowPosition(self, motor, speed=0):
        if speed == 0:
            speed = self.travel_velocity
        logger.info("gun %d, motor, motor: %s, speed" % \
                    (self.instance_number, motor, speed))
        yield from bps.mv(motor.velocity, speed)
        yield from motor.mv(self.low_position)

    def goToHighPosition(self, motor, speed=0):
        if speed == 0:
            speed = self.travel_velocityinstance_number
        logger.info("gun %d, motor, motor: %s, speed" % \
                    (self.instance_number, motor, speed))
        yield from bps.mv(motor.velocity, speed)
        yield from motor.mv(self.high_position)
        
        
    def enable(self):
        #logger.info("gun number %d" % d)
        yield from bps.abs_set(self.relay_magnetron, True)     

    def disable(self):
        #logger.info("gun number %d" % d)
        yield from bps.abs_set(self.relay_magnetron, False)     



class GunSelector(DepositionListDevice):
    DISABLE_TEXT = 0
    ENABLE_TEXT = 1
    PS_LOW_LEVEL_TEXT = 'ps_low_level'
    current_active_gun = FC(EpicsSignal, "{self.prefix}:userCalcOut10.A", 
                            name="current_active_gun",
                            put_complete=True)
    power_on = FC(EpicsSignal, "{self.prefix}:plc:MPS1_Magnetron_Power_RB",
                     write_pv="{self.prefix}:plc:MPS1_Mag_Pwr_On_OUT",
                     name="mps1_power_on",
                     string=True,
                     put_complete=True)
    mps1_enable_output = FC(EpicsSignal, "{self.prefix}:ION:1:set_enable.PROC",
                        name="mps1_enable_output",
                        #string=True,
                        put_complete=True)
    mps1_disable_output = FC(EpicsSignal, "{self.prefix}:ION:1:set_disable.PROC",
                         name="mps1_disable_output",
                         #string=True,
                         put_complete=True)
    ps1_voltage = FC(EpicsSignal, "{self.prefix}:userCalc8",
                     write_pv="{self.prefix}:userCalc5.A",
                     name = "ps1_ps_voltage", 
                     string=True,
                     put_complete=True)
    ps1_current = FC(EpicsSignal, "{self.prefix}:userCalc10",
                     write_pv="{self.prefix}:userCalc7.A",
                     name="ps1_ps_current",
                     string=True,
                     put_complete=True)
    ps1_power = FC(EpicsSignal, "{self.prefix}:userCalc9",
                   write_pv="{self.prefix}:userCalc6.A",
                   name="ps1_ps_power",
                   string=True,
                   put_complete=True)
    mps1_voltage = FC(EpicsSignal, "{self.prefix}:ION:1:target_voltage_sp_rd",
                     write_pv="{self.prefix}:ION:1:voltage",
                     name = "mps1_ps_voltage", 
                     string=True,
                     put_complete=True)
    mps1_current = FC(EpicsSignal, "{self.prefix}:ION:1:target_current_sp_rd",
                     write_pv="{self.prefix}:ION:1:current",
                     name="mps1_ps_current",
                     string=True,
                     put_complete=True)
    mps1_power = FC(EpicsSignal, "{self.prefix}:ION:1:target_power_sp_rd",
                   write_pv="{self.prefix}:ION:1:power",
                   name="mps1_ps_power",
                   string=True,
                   put_complete=True)
    mps1_voltage_rbv = FC(EpicsSignal, "{self.prefix}:ION:1:volts_rd",
                     name = "mps1_ps_voltage_rbv", 
                     string=True,
                     put_complete=True)
    mps1_current_rbv = FC(EpicsSignal, "{self.prefix}:ION:1:amps_rd",
                     name="mps1_ps_current_rbv",
                     string=True,
                     put_complete=True)
    mps1_power_rbv = FC(EpicsSignal, "{self.prefix}:ION:1:watts_rd",
                   name="mps1_ps_power_rbv",
                   string=True,
                   put_complete=True)
    guns = DDC(_gun_fields('', 'gun',  range(1, 9)))
    logger.debug("guns %s" %guns)

    def __init__(self, *args, **kwargs):
        logger.error("__init__ for GunSelector")
        prefix = args[0]
        self.number_of_guns = NUMBER_OF_GUNS
        super(GunSelector, self).__init__(*args, **kwargs)
        
    def disable_gun(self, gun_number, ps_low_level=5.0, override=False):
        done_status = DeviceStatus(self)
        logger.info("Disabling gun %d" % gun_number)
        gun_to_disable = self.guns.__getattr__("gun%d" % gun_number)
        current_active_gun = self.current_active_gun.get()
        if (current_active_gun == gun_number) or (override == True):
            logger.debug("Disable the active gun")
            self.mps1_disable_output.set(self.ENABLE_TEXT)
            self.mps1_disable_output.set(self.DISABLE_TEXT)
            def verify_ps1_voltage_cb(value, timestamp, **kwargs):
                logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                            (ps_low_level, value))
                if value < ps_low_level:
                    logger.info("ps1 has been disabled")
                    # Once the power supply goes below ps_low_level disable it
                    gun_to_disable.relay_magnetron.set(self.DISABLE_TEXT)
                    logger.info("Gun %d is disabled")
                    self.current_active_gun.set(0.0)
                    self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                    done_status._finished()
            self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        else:
            logger.info("Request to disable gun %d but it is not the " \
                        "current_active_gun. Use override=True to force " \
                        "disable" % gun_number)
        
    def disable_all_guns(self, ps_low_level=5):
        logger.info("Disabling all guns")
        done_status = DeviceStatus(self)

        current_active_gun = self.current_active_gun.get()
        self.mps1_disable_output.set(self.ENABLE_TEXT)
        self.mps1_disable_output.set(self.DISABLE_TEXT)
        def verify_ps1_voltage_cb(value, timestamp, **kwargs):
            logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if value < ps_low_level:
                logger.info("ps1 has been disabled")
                # Once the power supply goes below ps_low_level disable it
                for gun_index in range(1,9):
                    gun_to_disable = self.guns.__getattr__("gun%d" % gun_index)
                    gun_to_disable.relay_magnetron.set(self.DISABLE_TEXT)
                self.current_active_gun.set(0.0)
                logger.info("All guns are disabled")
                self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                done_status._finished()
        self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        
    def enable_gun(self, gun_number, ps_low_level=5.0):
        done_status = DeviceStatus(self)
        #Before enabling the relay
        self.mps1_disable_output.set(self.ENABLE_TEXT)
        self.mps1_disable_output.set(self.DISABLE_TEXT)
        current_active_gun = int(self.current_active_gun.get())
        gun_to_enable = self.guns.__getattr__("gun%d" % gun_number)
        if current_active_gun != 0:
            gun_current = self.guns.__getattr__("gun%d" % current_active_gun)
        logger.info("Enabling gun %d, current_active_gun %d" % \
              (gun_number, current_active_gun))
        def verify_ps1_voltage_cb(value, timestamp, **kwargs):
            value=float(value)
            logger.info("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if float(value) < float(ps_low_level):
                print("ps1 has been disabled")
                # Once the power supply goes below ps_low_level enable it
                if current_active_gun !=0:
                    
                    if gun_number != current_active_gun:
                        logger.info("Disabling gun %d which is already active" % \
                                    current_active_gun)
                        gun_current.relay_magnetron.set(self.DISABLE_TEXT)
                        self.current_active_gun.set(0)
                        logger.info("Enabling gun %d which was requested" % \
                                    gun_number)
                        gun_to_enable.relay_magnetron.set(self.ENABLE_TEXT)
                        self.current_active_gun.set(gun_number)
                    else:
                        logger.info("Enabling gun %d which is the current_active gun" %
                                    gun_number)
                        gun_state = gun_to_enable.relay_magnetron.get()
                        if gun_state == self.ENABLE_TEXT:
                            logger.info("Gun is already enabled")
                        else:
                            logger.info("Gun %d is disabled need to enable it" %
                                        gun_number)
                            gun_to_enable.relay_magnetron.set(self.ENABLE_TEXT)    
                        self.current_active_gun.set(gun_number)
                else:
                    gun_to_enable.relay_magnetron.set(self.ENABLE_TEXT)
                    self.current_active_gun.set(gun_number)
                    
                self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                done_status._finished()
        # go into the waiting loop.
        self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        return done_status

    def disable_all_guns(self, ps_low_level=5):
        logger.info("Disabling all guns")
        done_status = DeviceStatus(self)

        current_active_gun = self.current_active_gun.get()
        self.mps1_disable_output.set(self.ENABLE_TEXT)
        self.mps1_disable_output.set(self.DISABLE_TEXT)
        def verify_ps1_voltage_cb(value, timestamp, **kwargs):
            logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if value < ps_low_level:
                logger.info("ps1 has been disabled")
                # Once the power supply goes below ps_low_level disable it
                for gun_index in range(1,9):
                    gun_to_disable = self.guns.__getattr__("gun%d" % gun_index)
                    gun_to_disable.relay_magnetron.set(self.DISABLE_TEXT)
                self.current_active_gun.set(0.0)
                logger.info("All guns are disabled")
                self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                done_status._finished()
        self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        return done_status
    
            
    def mps1_disable(self):
        logger.info("disable_power_supply")
        self.mps1_disable_output.set(self.ENABLE_TEXT)
        self.mps1_disable_output.set(self.DISABLE_TEXT)
        #Add verify power is down.
        def verify_ps1_voltage_cb(value, timestamp, **kwargs):
            logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if value < ps_low_level:
                logger.info("ps1 has been disabled")
                self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                done_status._finished()
        self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        return done_status
        
    def mps1_enable(self):
        logger.debug("enable_power_supply")
        self.mps1_enable_output(self.ENABLE_TEXT)
        self.mps1_enable_output(self.DISABLE_TEXT)
        disable
        
    def mps1_power_on(self):
        logger.debug("mps1_power_on")
        yield from bps.mv(self.power_on, True)
        
    def mps1_power_off(self):
        logger.debug("enable_power_on")
        yield from bps.mv(self.power_on, False)
        
    def set(self, gun, **kwargs):
        '''
        Sets the active gun.  Before switching guns, need to ensure that the 
        no guns are receiving power above a threshold value.  The threshold 
        value may be set by including the keyword argument 'ps_low_level'.  
        If this is missing thentype filter text a value of 5V is used.  
        Gun number should be between 0 and 8.  If 0 is selected, then all 
        guns are disabled including the current active gun and the current
        active gun is set to 0.  
        Note that any attempt to switch guns will first ensure that the 
        output of the power supply has ramped below the threshold.  The 
        disable output signal is triggered to force the power supply to start
        ramping to zero.  No changes are made to the gun relay magnetrons are
        made until the voltage is below the threshold.  Also note, that after 
        the switching of guns, the gun voltage remains disabled.  The user code
        must enable the power supply output before using the gun.
        '''
        logging.info ("Setting gun %d" % gun)
        if gun > 8 or gun <0:
            raise(RuntimeError("Invalid gun selected gun number must be"
                               " between 0 & 8."))
        ps_low_level = 5.0
        # Check if the user has changed the ps_low_level which controls 
        # when relays can be switched.
        if self.PS_LOW_LEVEL_TEXT in kwargs:
            ps_low_level = kwargs[self.PS_LOW_LEVEL_TEXT]
        print (ps_low_level)
        if gun == 0:
            return self. disable_all_guns()
        else:
            return self.enable_gun(gun, ps_low_level=ps_low_level)
        

        