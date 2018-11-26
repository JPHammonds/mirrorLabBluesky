import logging
import bluesky.plan_stubs as bps
from ophyd.ophydobj import Kind
from ophyd.signal import EpicsSignal, Signal
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC, FormattedComponent as FC)
import csv
from _collections import OrderedDict
import logging.config
from ophyd.status import DeviceStatus
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
        logging.config.fileConfig(logConfigFile, disable_existing_loggers=False )
        print("Success Openning logfile")
    except (NoSectionError,TypeError) as ex:
        print ("In Exception to load dictConfig package %s Because of exeption\n  %s" % (LOGGER_NAME, ex))
        logging.config.dictConfig(LOGGER_DEFAULT)
    except KeyError as ex:
        print ("logfile %s was missing or had errant sections %s" %(logConfigFile, ex.args))
else:
    logging.config.dictConfig(LOGGER_DEFAULT)
logger = logging.getLogger(LOGGER_NAME)
        

print("__name__: %s" %__name__)
 
NUMBER_OF_GUNS = 8
CONFIG_FIELDS = ["object", "channel_name", "pv", "write_pv", "description", "name"]

def testDepositionListDevice():
    dev = DepositionListDevice("test:", instance_number=1, config_file='pv_map.csv')
    logger.debug (dev.configuration)
    print (dev.__class__)
    
class DepositionListDevice(Device):
    def __init__(self, *args, instance_number=0, config_file="", **kwargs):
        self.prefix = args[0]
        self.instance_number=instance_number
        self.instance_letter=chr(instance_number+64)
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
        
    

class LandingChamber(DepositionListDevice):
    cryo_power_on = FC(EpicsSignal, "{self.prefix}:plc:CP1_Landing_Chamber_Cryo_Pump_RB",
               write_pv='{self.prefix}:plc:CP1_LC_Cryo_Pump_Off_OUT',
               string=True,
               name = 'cryo_power_on')
    cryo_exhaust_to_vp1 = FC(EpicsSignal, '{self.prefix}:plc:CP1_Exhaust_to_VP1_RB',
                           write_pv='{self.prefix}:plc:CP1_Exhaust_VP1_On_OUT',
                           
                           string=True,
                           name = 'cryo_exhaust_to_vp1')
    cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_5_IN",
                    name = 'cryo_pressure')
    cryo_temperature_status = FC(EpicsSignal, "{self.prefix}:plc:Cryo_Pump_1_ok_IN",
                            string=True,
                            name= 'cryo_temperature_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP1_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP1_OUT",
                  name = 'n2_purge',
                  string=True)
    ccg_power_on = FC(EpicsSignal, "{self.prefix}:plc:Landing_Chamber_CCG1_RB",
                  write_pv = "{self.prefix}:plc:LC_CCG1_Enable_OUT",
                  name = 'ccg_power_on',
                  string=True)
    ccg_pressure = FC(EpicsSignal,
                      '{self.prefix}:plc:CCG_1_IN',
                      name='ccg_pressure')
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_1_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_1_Pos_OUT",
                             name='gate_valve_position')
    gate_valve_close_request = FC(EpicsSignal, \
                                  "{self.prefix}:plc:Landing_Chamber_Cryo_GV1_CLOSED_RB", \
                                  write_pv="{self.prefix}:plc:LC_Cryo_GV1_Close_OUT", \
                                  name = 'gate_valve_close_request', \
                                  string='True')
    gate_valve_open_request = FC(EpicsSignal, \
                                 "{self.prefix}:plc:Landing_Chamber_Cryo_GV1_OPEN_RB", \
                                 write_pv="{self.prefix}:plc:LC_Cryo_GV1_Open_OUT", \
                                 name='gate_valve_open_request', \
                                 string=True)
    gate_valve_fully_closed = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LC_GV1_DoorClosed_IN', \
                                 name = 'gate_valve_fully_closed', \
                                 string=True)
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:LC_GV1_DoorOpen_IN', \
                                 name = 'gate_valve_fully_open', \
                                 string=True)
    
    
class PlanarChamber(DepositionListDevice):
    cryo_power_on = FC(EpicsSignal,
                             '{self.prefix}:plc:CP2_Planar_Chamber_Cryo_Pump_RB',
                             write_pv='{self.prefix}:plc:CP2_PC_Cryo_Pump_Off_OUT',
                             name='cryo_power_on',
                             string=True)
    cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_6_IN",
                    name = 'cryo_pressure')
    cryo_temperature_status = FC(EpicsSignal, "{self.prefix}:plc:Cryo_Pump_2_ok_IN",
                            string=True,
                            name='cryo_temp_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP2_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP2_OUT",
                  name = 'n2_purge',
                  string=True)
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_2_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_2_Pos_OUT",
                             name='gate_valve_position')
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
                                 name = 'gate_valve_fully_closed', \
                                 string=True)
    gate_valve_fully_open = FC(EpicsSignal, \
                                 '{self.prefix}:plc:RC_GV2_Open_IN', \
                                 name = 'gate_valve_fully_open', \
                                 string=True)
    cryo_exhaust_to_vp1 = FC(EpicsSignal, \
                             '{self.prefix}:plc:CP2_Exhaust_to_VP1_RB',
                             write_pv='{self.prefix}:plc:CP2_Exhaust_VP1_On_OUT',
                             name='cryo_exhaust_to_vp1',
                             string=True
                            )
    
class RoundChamber(DepositionListDevice):
    cryo_power_on = FC(EpicsSignal,
                             '{self.prefix}:plc:CP3_Round_Chamber_Cryo_Pump_RB',
                             write_pv='{self.prefix}:plc:CP3_RC_Cryo_Pump_Off_OUT',
                             name='cryo_power_on',
                             string=True)
    cp_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_7_IN",
                    name = 'cp3_pressure')
    cryo_temperature_status = FC(EpicsSignal, "{self.prefix}:plc:Cryo_Pump_3_ok_IN",
                                 string=True,
                                 name='cryo_temperature_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP3_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP3_OUT",
                  name = 'n2_purge',
                  string=True)
    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_3_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_3_Pos_OUT",
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
    cryo_exhaust_to_vp1 = FC(EpicsSignal, \
                             '{self.prefix}:plc:CP3_Exhaust_to_VP1_RB',
                             write_pv='{self.prefix}:plc:CP3_Exhaust_VP1_On_OUT',
                             name='cryo_exhaust_to_vp1',
                             string=True
                            )

class LoadlockChamber(DepositionListDevice):
    cryo_power_on = FC(EpicsSignal,
                             '{self.prefix}:plc:CP4_Loadlock_Chamber_Cryo_Pump_RB',
                             write_pv='{self.prefix}:plc:CP4_LLC_Cryo_Pump_Off_OUT',
                             name='cryo_power_on',
                             string=True)
    cryo_pressure = FC(EpicsSignal, "{self.prefix}:plc:PT_8_IN",
                    name = 'cryo_pressure')
    cryo_temperature_status = FC(EpicsSignal, "{self.prefix}:plc:Cryo_Pump_4_ok_IN",
                                 string=True,
                                 name='cryo_temperature_status')
    cryo_exhaust_to_vp1 = FC(EpicsSignal, \
                             '{self.prefix}:plc:CP4_Exhaust_to_VP1_RB',
                             write_pv='{self.prefix}:plc:CP4_Exhaust_VP1_On_OUT',
                             name='cryo_exhaust_to_vp1',
                             string=True
                            )
    n2_purge = FC(EpicsSignal, "{self.prefix}:plc:N2_Purge_to_CP4_RB",
                  write_pv="{self.prefix}:plc:N2_Purge_CP4_OUT",
                  name = 'n2_purge',
                  string=True)
    ccg_power_on = FC(EpicsSignal, "{self.prefix}:plc:Loadlock_CCG2_RB",
                   write_pv = "{self.prefix}:plc:LL_CCG2_Enable_OUT",
                 name='power_on',
                   string=True)
    ccg_pressure = FC(EpicsSignal,
                      '{self.prefix}:plc:CCG_2_IN')

    gate_valve_position = FC(EpicsSignal, "{self.prefix}:plc:GV_4_Pos_IN",
                             write_pv="{self.prefix}:plc:GV_4_Pos_OUT",
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
                                 string=True)
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
                               name='ar_backfill_high_rate',
                               string=True)
    ar_backfill_low_rate = FC(EpicsSignal,
                              '{self.prefix}:plc:Ar_Backfill_to_LL_RB',
                              write_pv='{self.prefix}:plc:Ar_Backfill_LL_On_OUT',
                              name='ar_backfill_low_rate',
                              string=True)                   

class CenterChamber(DepositionListDevice):
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
    flow = FC(EpicsSignal, "{self.prefix}:plc:MFC_{self.instance_number}_IN",
               write_pv="{self.prefix}:plc:MFC_{self.instance_number}_OUT", 
                          kind=Kind.config)
    valve_on = FC(EpicsSignal, "{self.prefix}:plc:MFC{self.instance_number}_RB",
                  write_pv = "{self.prefix}:plc:MFC{self.instance_number}_RC_On_OUT", 
                          kind=Kind.config,
                          string=True)
    plc_bypass = FC(EpicsSignal, "{self.prefix}:plc:MFC{self.instance_number}_Manual_OUT",
                     write_pv = "{self.prefix}:plc:MFC{self.instance_number}_Manual_OUT", 
                          kind=Kind.config, 
                          string=True)
    epics_pid_control = FC(EpicsSignal, '{self.prefix}:userCalc1.{self.instance_letter}',
                            write_pv = '{self.prefix}:userCalc1.{self.instance_letter}' , 
                          kind=Kind.config,
                          string=True)

    def __init__(self, *args, ch_name=None, mixerNumber=0, mixtureID="", \
                 flow=0, **kwargs):
        self.chName = ch_name
        self.mixtureID = mixtureID
        super(MassFlowControl, self).__init__(*args, **kwargs)
        depos_sys.gun_selector.ps1_voltage
    def close_valve(self, group=None, wait=False):
        yield from bps.abs_set(self.valve_on, 0, group=group, wait=wait)
        
    def disable_epics_pid_control(self, group=None, wait=False):
        yield from bps.mv(self.epics_pid_control,0,group=group, wait=wait)
        
    def disable_plc_bypass(self, group=None, wait=False):
        yield from bps.mv(self.plc_bypass, 0, group=group, wait=False)
        
    def enable_epics_pid_control(self, group=None, wait=False):
        yield from bps.mv(self.epics_pid_control, 1, group=group, wait=wait)
        
    def enable_plc_bypass(self, group=None, wait=False):
        yield from bps.mv(self.plc_bypass, 1, group=group, wait=wait)
        
    def open_valve(self, group=None, wait=False):
        yield from bps.mv(self.valve_on, 1, group=group, wait=wait)
        
    def set_flow(self, new_flow, group=None, wait=False):
        yield from bps.mv(self.flow, new_flow, group=group, wait=wait)
        
    def purge(self, leak_rate, low_check_value, group=None, wait=False):
        done_status = DeviceStatus(self)
        yield bps.abs_set(self.flow, leak_rate, group=group, wait=wait)
        def purge_done_cb(value, timestamp, **kwargs):
            if value < low_check_value:
                self.flow.clear_sub(purge_done_cb)
                done_status._finished()
        self.flow.subscribe(purge_done_cb)
        return done_status
            

def _mfc_fields( prefix, field_base, range_, **kwargs):
    defn = OrderedDict()
    
    for i in range_:
        suffix = '{field}{i}'.format(field=field_base, i=i)
        #kwargs['instance_number'] = i
        #kwargs['instance_letter'] = chr(i+64)
        defn['{}{}'.format(field_base, i)] = (MassFlowControl, prefix, {'instance_number':i, 'kind':Kind.normal})
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
        logger.info("Closing valves for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.close_valve(group='close_valves')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='close_valves')
        
    def close_mixed_gas_relays(self, relay_nums=None):
        if relay_nums is None:
            relay_nums=range(1, 9)
        for relay in relay_nums:
            relay_name = self.MIXED_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name), self.RELAY_CLOSE_TEXT,
                                   group='close_mixed_gas_relays')
        yield from bps.wait(group='close_mixed_gas_relays')
    
    def close_argon_gas_relays(self, relay_nums=None):
        if relay_nums is None:
            relay_nums=range(1, 9)
        for relay in relay_nums:
            relay_name = self.ARGON_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name), 
                                   self.RELAY_CLOSE_TEXT,
                                   group='close_argon_gas_relays')
        yield from bps.wait(group='close_mixed_gas_relays')
    
        
    def disable_mfc_plc_bypass(self):
        logger.info("Disabling plc_bypass for all MFCs")
        for mfc_name in self.mfcs.component_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.disable_plc_bypass(group='disable_plc_bypass')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='disable_plc_bypass')
            
    def disable_mfc_epics_pid_control(self, mfc_names=None):
        logger.info("Disabling epics_pid_control for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
            
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.disable_epics_pid_control(group='diable_pid_control')
            logger.debug("mfc % s" % mfc )
        yield from bps.wait(group='diable_pid_control')
        
    def enable__mfc_plc_bypass(self, mfc_names=None):
        logger.info("Enabling plc_bypass for all MFCs")
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.enable_plc_bypass(group='enable_plc_bypass')
            logger.debug("mfc % s" % mfc )
        bps.wait(group='enable_bps_bypass')
            
    def open_mixed_gas_relays(self, relay_nums=None):
        if relay_nums is None:
            relay_nums=range(1, 9)
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
        if relay_nums is None:
            relay_nums=range(1, 9)
        for relay in relay_nums:
            relay_name = self.ARGON_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name),
                                   self.RELAY_OPEN_TEXT,
                               group='open_argon_gas_relays')
        yield from bps.wait(group='open_argon_gas_relays')
    
    def set_mfc_flows(self, new_flow, mfcs_names=None):
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.set_flow(new_flow,group='set_flows')
        yield from bps.wait('set_flows')
        
    def purge_mfcs(self, mfc_names=None, leak_rate=25, low_value=5):
        
        if mfc_names == None:
            mfc_names=self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.purge(leak_rate, low_value, group='purge_mfcs')
        bps.wait('purge_mfcs')
    
def _gun_fields( prefix, field_base, range_, **kwargs):
    defn = OrderedDict()
    
    for i in range_:
        suffix = '{field}{i}'.format(field=field_base, i=i)
        kwargs['instance_number'] = i
        defn['{}{}'.format(field_base, i)] = (Gun, prefix, {'instance_number':i, 'kind':Kind.normal})
    return defn

class Gun(DepositionListDevice):
    # Configure these as FormattedComponents
    relay_magnetron = FC(EpicsSignal, "{self.prefix}:plc:Magnetron_{self.instance_number}_Power_RB",
                          write_pv="{self.prefix}:plc:Mag{self.instance_number}_Pwr_Enable_OUT",
                          name="relay_magnetron",
                          string=True,
                          put_complete=True, 
                          kind=Kind.config)
    voltage_avg = FC(EpicsSignal, "{self.prefix}:userAve{self.instance_number}.VAL",
                      name='voltage_avg', 
                          kind=Kind.config)
    water_flow_cathode_raw = FC(EpicsSignal, "{self.prefix}w:USB231:1:Ai{self.instance_number}",
                                 name='water_flow_cathode_raw', 
                          kind=Kind.config)
    water_flow_cathode = FC(EpicsSignal, "{self.prefix}:userCalcOut1{self.instance_number}.VAL",
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
#         self.high_position = self.zero_position - self.sample_upper_extent - self.mask_width/self.overspray
#         self.low_position = self.zero_position - self.sample_lower_extent - self.mask_width/self.overspray
        super(Gun, self).__init__(*args, **kwargs)
        self.high_position.put(self.zero_position.value - self.sample_upper_extent - self.mask_width.value/self.overspray)
        self.low_position.put(self.zero_position.value - self.sample_lower_extent - self.mask_width.value/self.overspray)
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
    DISABLE_TEXT = 'Disable'
    ENABLE_STATUS = 'Enable'
    current_active_gun = FC(EpicsSignal, "{self.prefix}:userCalcOut10.A",    def enable_relay5(self, ps_low_level=5.0):
        yield from self.enable_relay_magnetron(5, \
                                               ps_low_level=ps_low_level)


                            write_pv="{self.prefix}:userCalcOut10.A",
                            name="current_active_gun")
    power_on = FC(EpicsSignal, "{self.prefix}:plc:MPS1_Magnetron_Power_RB",
                     write_pv="{self.prefix}:plc:MPS1_Mag_Pwr_On_OUT",
                     name="mps1_power_on",
                     string=True,
                     put_complete=True)
    enable_output = FC(EpicsSignal, "{self.prefix}:ION:1:set_enable.PROC",
                        name="mps1_enable_output",
                        string=True,
                        put_complete=True)
    disable_output = FC(EpicsSignal, "{self.prefix}:ION:1:set_disable.PROC",
                         name="mps1_disable_output",
                         string=True,
                         put_complete=True)
    ps_voltage = FC(EpicsSignal, "{self.prefix}:ION:1:target_voltage_sp_rd",
                     write_pv="{self.prefix}:ION:1:voltage",
                     name = "mps1_ps_voltage", 
                     string=True,
                     put_complete=True)
    ps_current = FC(EpicsSignal, "{self.prefix}:ION:1:target_current_sp_rd",
                     write_pv="{self.prefix}:ION:1:current",
                     name="mps1_ps_current",
                     string=True,
                     put_complete=True)
    ps_power = FC(EpicsSignal, "{self.prefix}:ION:1:target_power_sp_rd",
                   write_pv="{self.prefix}:ION:1:power",
                   name="mps1_ps_power",
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
            self.mps1_disable_output.set(self.DISABLE_RELAY_TEXT)
            def verify_mps1_voltage_cb(value, timestamp, **kwargs):
                logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                            (ps_low_level, value))
                if value < ps_low_level:
                    logger.info("ps1 has been disabled")
                    # Once the power supply goes below ps_low_level disable it
                    gun_to_disable.relay_magnetron.set(self.DISABLE_RELAY_TEXT)
                    logger.info("Gun %d is disabled")
                    self.current_active_gun.set(0.0)
                    self.ps1_voltage.clear_sub(verify_mps1_voltage_cb)
                    done_status._finished()
            self.ps1_voltage.subscribe(verify_mps1_voltage_cb)
        else:
            logger.info("Request to disable gun %d but it is not the " \
                        "current_active_gun. Use override=True to force " \
                        "disable" % gun_number)
        
    def disable_all_guns(self, ps_low_level=5):
        logger.info("Disabling all guns")
        done_status = DeviceStatus(self)

        current_active_gun = self.current_active_gun.get()
        self.mps1_disable_output.set(self.DISABLE_RELAY_TEXT)
        def verify_mps1_voltage_cb(value, timestamp, **kwargs):
            logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if value < ps_low_level:
                logger.info("ps1 has been disabled")
                # Once the power supply goes below ps_low_level disable it
                for gun_index in range(1,9):
                    gun_to_disable = self.guns.__getattr__("gun%d" % gun_index)
                    gun_to_disable.relay_magnetron.set(self.DISABLE_RELAY_TEXT)
                self.current_active_gun.set(0.0)
                logger.info("All guns are disabled")
                self.ps1_voltage.clear_sub(verify_mps1_voltage_cb)
                done_status._finished()
        self.ps1_voltage.subscribe(verify_mps1_voltage_cb)
        
    def disable_gun(self, gun_number, ps_low_level=5.0, override=False):
        done_status = DeviceStatus(self)
        logger.info("Disabling gun %d" % gun_number)
        gun_to_disable = self.guns.__getattr__("gun%d" % gun_number)
        current_active_gun = self.current_active_gun.get()
        if (current_active_gun == gun_number) or (override == True):
            self.mps1_disable_output.set(self.DISABLE_RELAY_TEXT)
            def verify_mps1_voltage_cb(value, timestamp, **kwargs):
                logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                            (ps_low_level, value))
                if value < ps_low_level:
                    logger.info("ps1 has been disabled")
                    # Once the power supply goes below ps_low_level disable it
                    gun_to_disable.relay_magnetron.set(self.DISABLE_RELAY_TEXT)
                    logger.info("Gun %d is disabled")
                    self.current_active_gun.set(0.0)
                    self.ps1_voltage.clear_sub(verify_mps1_voltage_cb)
                    done_status._finished()
            self.ps1_voltage.subscribe(verify_mps1_voltage_cb)
        else:
            logger.info("Request to disable gun %d but it is not the " \
                        "current_active_gun. Use override=True to force " \
                        "disable" % gun_number)
        
    def disable_all_guns(self, ps_low_level=5):
        logger.info("Disabling all guns")
        done_status = DeviceStatus(self)

        current_active_gun = self.current_active_gun.get()
        self.mps1_disable_output.set(self.DISABLE_RELAY_TEXT)
        def verify_mps1_voltage_cb(value, timestamp, **kwargs):
            logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if value < ps_low_level:
                logger.info("ps1 has been disabled")
                # Once the power supply goes below ps_low_level disable it
                for gun_index in range(1,9):
                    gun_to_disable = self.guns.__getattr__("gun%d" % gun_index)
                    gun_to_disable.relay_magnetron.set(self.DISABLE_RELAY_TEXT)
                self.current_active_gun.set(0.0)
                logger.info("All guns are disabled")
                self.ps1_voltage.clear_sub(verify_mps1_voltage_cb)
                done_status._finished()
        self.ps1_voltage.subscribe(verify_mps1_voltage_cb)
        
    
            
    def disable_power_supply(self):
        logger.info("disable_power_supply")
        yield from bps.mv(self.disable_output, True)
        #Add verify power is down.
        
    def enable_power_supply(self):
        logger.debug("enable_power_supply")
        yield from bps.mv(self.enable_output, True)
        
    def mps1_power_enable(self):
        logger.debug("mps1_power_on")
        yield from bps.mv(self.power_on, True)
        
    def mps1_power_disable(self):
        logger.debug("enable_power_on")
        yield from bps.mv(self.power_on, False)
        
    def set(self, gun, **kwargs):
        logging.info ("Setting gun %d" % gun)
        ps_low_level = 5.0
        if 'ps_low_level' in kwargs:
            ps_low_level = kwargs['ps_low_level']
        print (ps_low_level)
        return self.enable_gun(gun, ps_low_level=ps_low_level)
        

        