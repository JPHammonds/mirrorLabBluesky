print(__file__)
from ophyd import Signal
from ophyd import Device
#from ophyd import Component as Cpt
from ophyd.device import ALL_COMPONENTS
# Set up default complex devices

class DepositionSystem(Device):
    ENABLE = 'Enable'
    DISABLE = 'Disable'
    MAINTENANCE = 'Maintenance'
    RUNNING = 'RUNNING'
    IOC_REBOOT = 'IOC Reboot'
    VALVE_ALL_OPEN = 100.0
    m1 = Cpt(EpicsMotor, ':m1', name='m1')
    gun_selector = Cpt(GunSelector, "")
    gas_mixer = Cpt(GasMixer, "")
    landing_chamber = Cpt(LandingChamber, "")
    planar_chamber = Cpt(PlanarChamber, "")
    round_chamber = Cpt(RoundChamber, "")
    loadlock_chamber = Cpt(LoadlockChamber, "")
    center_chamber = Cpt(CenterChamber, "")
    vp1_substitutions = {'speed_read_pv_suffix': ':plc:VFD_1_IN',
                         'speed_write_pv_suffix': ':plc:VFD_1_OUT',
                         'n2_purge_read_pv_suffix': ':plc:EOV5_N2_Purge_to_VP1_RB',
                         'n2_purge_write_pv_suffix': ':plc:N2_Purge_VP1_Open_OUT',
                         'power_on_read_pv_suffix': ':plc:VP1_Process_Vacuum_Pump_RB',
                         'power_on_write_pv_suffix': ':plc:VP1_Process_Vacuum_Pump_RB',
                         'kind': Kind.normal}
    vp1 = Cpt(VariableFrequencyDrivePump, '', **vp1_substitutions)
    operation_status = Cpt(EpicsSignal, ":Operations_Status",
                           write_pv=':Operations_Status',
                           string=True,
                           name='operation_status')
    vp2_substitutions = {'power_on_read_pv_suffix': ':plc:EOV1_VP2_Seals_Pump_RB',
                         'power_on_write_pv_suffix': ':plc:VP2_Seals_Pump_On_OUT'}
    vp2 = Cpt(SealsPump, '', **vp2_substitutions)
    
    def close_vacuum_gate_valves(self):
        # set up valves to open
        yield from self.landing_chamber.gate_valve.gate_valve.close( group='gate_valves') 
        yield from self.planar_chamber.gate_valve.gate_valve.close( group='gate_valves') 
        yield from self.round_chamber.gate_valve.gate_valve.close( group='gate_valves') 
        yield from self.loadlock_chamber.gate_valve.gate_valve.close( group='gate_valves') 
        #wait for all of the valves to openshutdown
        yield from bps.wait(group='gate_valves')

    def disable_ccgs(self):
        '''
        Turns of Cold Cathode gauges in the Landing chamber and Load Lock
        chamber so that they cannot be damaged by gas flowing.
        '''
        yield from self.landing_chamber.disable_ccg(group='cathode_gauges')
        yield from self.loadlock_chamber.disable_ccg(group='cathode_gauges')
#        yield from bps.wait(group='cathode_gauges')
        
    def enable_ccgs(self):
        '''
        Enable the Cold Cathode Gauges.  i.e. after finishing a purge
        '''
        yield from self.landing_chamber.enable_ccg(group='cathode_gauges')
        yield from self.loadlock_chamber.enable_ccg(group='cathode_gauges')
        
    def set_operation_status(self, new_status):
        '''
        Valid values of new_status are:
            DepositionSystem.MAINTENANCE
            DepositionSystem.RUNNING
            DepositionSystem.IOC_REBOOT    try:
        '''
        yield from bps.mv(self.operation_status, new_status)
        
    def set_op_status_maintenance(self):
        yield from self.set_operation_status(self.MAINTENANCE)
        
    def set_op_status_running(self):
        yield from self.set_operation_status(self.RUNNING)
        
    def set_op_status_ioc_reboot(self):
        yield from self.set_operation_status(self.IOC_REBOOT)

    def open_vacuum_gate_valves(self, position=VALVE_ALL_OPEN):
        # set up valves to open
        yield from self.landing_chamber.gate_valve.gate_valve.open(position=position,
                                                   group='gate_valves')
        yield from self.planar_chamber.gate_valve.gate_valve.open(position=position,
                                                   group='gate_valves')
        yield from self.round_chamber.gate_valve.gate_valve.open(position=position,
                                                   group='gate_valves')
        yield from self.loadlock_chamber.gate_valve.gate_valve.open(position=position,
                                                   group='gate_valves')
        #wait for all of the valves to open
        yield from bps.wait(group='gate_valves')
    
    def pump_down(self):
        '''
        Pump down the chamber from atmosphere
        '''
        
        
    def purge_gas_port(self):
        '''
        Purge one or more Gas ports to prepare them for use.  
        '''
        yield from self.disable_ccgs()
        yield from self.set_operation_status(self.RUNNING)
        yield from self.open_vacuum_gate_valves()
        yield from self.gas_mixer.purge_mfcs()

    def startup(self):
        self.purge()
                
    def shutdown(self):
        self.open_vacuum_gate_valves(position=100)
        self.disable_ccgs()
        yield from self.gas_mixer.shutdown()
        self.set_operation_status(DepositionSystem.MAINTENANCE)
        
depos_sys = DepositionSystem(prefix="depo2", name='depSys', read_attrs=ALL_COMPONENTS)
 
for c in depos_sys.component_names:
    child = getattr(depos_sys, c)
    child.name = child.name[len(depos_sys.name) + 1:]
    
# for c in depos_sys.gun_selector.component_names:
#     child = getattr(depos_sys.gun_selector, c)
#     child.name = child.name[len(depos_sys.gun_selector.name) +1:]
print("Deposition System component names %s" % depos_sys.component_names)

# Add PVs to IOC to let the user see this in MEDM
class LayerState(Device):
    speed = Cpt(Signal)
    motor = Cpt(Signal)
    start_position = Cpt(Signal)
    end_position = Cpt(Signal)
    between_layer_time = Cpt(Signal)
    selected_gun = Cpt(Signal)
    number_of_passes = Cpt(Signal)
    description = Cpt(Signal)
    layer = Cpt(Signal)
    sub_layer = Cpt(Signal)

    def __init__(self, prefix, ch_name=None, **kwargs):
        self._ch_name = ch_name
        super().__init__(prefix, **kwargs)  
            
layer_state = LayerState(prefix="", name='layer')
# To allow turning plots back on show only the ones without strings
# layer_state.hints ()    This may present possibilities

for c in layer_state.component_names:
    child = getattr(layer_state, c)
    child.name = child.name[len(layer_state.name) + 1:]
