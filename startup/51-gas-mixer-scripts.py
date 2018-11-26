import logging
import bluesky.plan_stubs as bps


logger = logging.getLogger(LOGGER_NAME)
def purge_port_n(self, port_number):
    disable_ccgs()

def purge_cathode_mfcs():
    yield from disable_ccgs()
    bps.mv(depos_sys.operation_status, 1)
    
    bps.mv(depos_sys.landing_chamber.gate_valve_position, 100.)
    bps.mv(depos_sys.planar_chamber.gate_valve_position, 100.)
    bps.mv(depos_sys.round_chamber.gate_valve_position, 100.)
    bps.mv(depos_sys.load_lock_chamber.gate_valve_position, 100.)
    
    yield from depos_sys.gas_mixer.close_mixed_gas_relays()    
    yield from depos_sys.gas_mixer.close_argon_gas_relays()    
    
    yield from depos_sys.gas_mixer.open_all_mfc_valves()    
    
    yield from depos_sys.gas_mixer.enable_all_mfc_plc_bypass()
    yield from depos_sys.gas_mixer.disable_all_mfc_epics_pid_control()
    logging.info("All 4 gate valves set to 100%")
    logging.info("All upstream gas mixing relays are now closed")
    logging.info("All 8 cathode MFC valves are opened")
    

    yield from depos_sys.gas_mixer.set_all_mfc_flows(25)
    logging.info("Setting all MFCs to dump gas")
    yield from depos_sys.gas_mixer.wait_for_low_mfc_flow()
    logging.info("A;; MFCs have exhausted their supply")
    yield from depos_sys.gas_mixer.set_all_mfc_flows(0)
    
    yield from depos_sys.gas_mixer.close_all_mfc_Valves()
    
def GM_Ar_All_On():
    yield from depos_sys.gas_mixer.close_mixed_gas_relays()
    yield from depos_sys.gas_mixer.open_argon_gas_relays()
    
    