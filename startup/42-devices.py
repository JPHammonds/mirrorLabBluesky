print(__file__)
from ophyd import Signal
from ophyd import Device
#from ophyd import Component as Cpt
from ophyd.device import ALL_COMPONENTS
# Set up default complex devices

# FIXME: how to get the PVs to the inner parts?
# TODO: How to build this up from previously-configured motors?

#class SlitAxis(Device):
#	lo = Cpt(EpicsMotor, ''){self.prefix}
#	hi = Cpt(EpicsMotor, '')

#class XY_Slit(Device):
#	h = Cpt(SlitAxis, '')
#	v = Cpt(SlitAxis, '')

#slit1 = XY_Slit()
#m1_VELO = EpicsSignal("depo2:m1.VELO", put_complete=True)
class DepositionSystem(Device):
    ENABLE = 'Enable'
    DISABLE = 'Disable'
    MAINTENANCE = 'Maintenance'
    RUNNING = 'RUNNING'
    IOC_REBOOT = 'IOC Reboot'__get
    VALVE_ALL_OPEN = 100.0
    m1 = Cpt(EpicsMotor, ':m1', name='m1')
    gun_selector = Cpt(GunSelector, "")
    gas_mixer = Cpt(GasMixer, "")
    landing_chamber = Cpt(LandingChamber, "")
    planar_chamber = Cpt(PlanarChamber, "")
    round_chamber = Cpt(RoundChamber, "")
    loadlock_chamber = Cpt(LoadlockChamber, "")
    center_chamber = Cpt(CenterChamber, "")
    operation_status = Cpt(EpicsSignal, ":Operations_Status",
                           write_pv=':Operations_Status',
                           string=True,
                           name='operation_status')
    
    def disable_ccgs(self):
        '''{self.prefix}
        Turns of Cold Cathode gauges in the Landing chamber and Load Lock
        chamber so that they cannot be damaged by gas flowing.__get
        '''
        yield from bps.mv(self.landing_chamber.power_on, self.DISABLE)
        yield from bps.mv(self.load_lock_chamber.power_on, self.DISABLE)
        
    def enable_ccgs(self):
        '''
        Enable the Cold Cathode Gauges.  i.e. after finishing a purge{self.prefix}
        '''
        yield from bps.mv(self.landing_chamber.power_on, self.ENABLE)
        yield from bps.mv(self.load_lock_chamber.power_on, self.ENABLE)
        
    def set_operation_status(self, new_status):
        '''
        Valid values of new_status are:
            DepositionSystem.MAINTENANCE
            DepositionSystem.RUNNING
            DepositionSystem.IOC_REBOOT
        '''
        yield from bps.mv(self.operation_status, new_status)  

    def open_vacuum_gate_valves(self):
        # set up valves to openDepositionListDevice
        yield from bps.abs_set(self.landing_chamber.gate_valve_position,
                               self.VALVE_ALL_OPEN, group='gate_valves' )
        yield from bps.abs_set(self.planar_chamber.gate_valve_position,
                               self.VALVE_ALL_OPEN, group='gate_valves')
        yield from bps.abs_set(self.round_chamber.gate_valve_position,
                               self.VALVE_ALL_OPEN, group='gate_valves')
        yield from bps.abs_set(self.loadlock_chamber.gate_valve_position,
                               self.VALVE_ALL_OPEN, group='gate_valves')
        #wait for all of the valves to open
        yield from bps.wait(group='gate_valves')
    {self.prefix}
    def purge_gas_port(self):{self.prefix}
        '''
        Purge one or more Gas ports to prepare them for use.  
        '''
        yield from self.disable_ccgs()
        yield from self.set_operation_status(self.RUNNING)
        yield from self.open_vacuum_gate_valves()
        
        
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
