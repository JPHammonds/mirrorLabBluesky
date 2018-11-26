# # m1 = EpicsSignal('depo2:m1', \
# #     'auto_monitor' = True, \
# # )
# m1_val = EpicsSignalRO('depo2:m1.VAL', \
#     'auto_monitor' = True, \
# )
# m1_accel = EpicsSignal('depo2:m1.ACCL', \
#     'auto_monitor' = True, \
# )
# m1_velocity = EpicsSignal('depo2:m1_VELOCITYEGU_MON', \
#     'write_pv' = depo2:m1.VELO, \
# 'auto_monitor' = True, \
# )
# m1_enable = EpicsSignal('depo2:m1.m1_able.VAL', \
#     'write_pv' = depo2:m1.m1_able.VAL, \
# 'auto_monitor' = True, \
# )
# m1_torque_enable = EpicsSignal('depo2:m1.CNEN', \
#     'auto_monitor' = True, \
# )
# m1_position_error = EpicsSignal('depo2:m1.DIFF', \
#     'auto_monitor' = True, \
# )
# m1_encoder_rbv = EpicsSignal('depo2:m1.REP', \
#     'auto_monitor' = True, \
# )
# m1_torque_output = EpicsSignal('depo2:Galil_Torque', \
#     'auto_monitor' = TrupicsSignalRO('depo2:m1_ESTALL_STATUS')
# m1_error = EpicsSignalRO('depo2:m1_ERR_MON')
# m1_encoder_stall_time = EpicsSignal('depo2:m1_ESTALLTIME_MON', \
#     'write_pv' = depo2:m1_ESTALLTIME_SP, \
# 'auto_monitor' = True, \
# )
# m1_execute_profile = EpicsSignal('depo2:Prof1:Execute')
# m1_build_profile = EpicsSignal('depo2:Prof1:Build')
# m1_profile_time = EpicsSignal('depo2:Prof1:FixedTime')
# operation_status = EpicsSignal('depo2:Operations_Status', \
#     'write_pv' = depo2:Operations_Status, \
# )
# relay_magnetron = {}
# relay_magnetron[1] = EpicsSignal('depo2:plc:Magnetron_1_Power_RB', \
#     write_pv = 'depo2:plc:Mag1_Pwr_Enable_OUT', \
# )
# relay_magnetron[2] = EpicsSignal('depo2:plc:Magnetron_2_Power_RB', \
#     write_pv = 'depo2:plc:Mag2_Pwr_Enable_OUT', \
# )
# relay_magnetron[3] = EpicsSignal('depo2:plc:Magnetron_3_Power_RB', \
#     write_pv = 'depo2:plc:Mag3_Pwr_Enable_OUT', \
# )
# relay_magnetron[4] = EpicsSignal('depo2:plc:Magnetron_4_Power_RB', \
#     write_pv = 'depo2:plc:Mag4_Pwr_Enable_OUT', \
# )
# relay_magnetron[5] = EpicsSignal('depo2:plc:Magnetron_5_Power_RB', \
#     write_pv = 'depo2:plc:Mag5_Pwr_Enable_OUT', \
# )
# relay_magnetron[6] = EpicsSignal('depo2:plc:Magnetron_6_Power_RB', \
#     write_pv = 'depo2:plc:Mag6_Pwr_Enable_OUT', \
# )
# relay_magnetron[7] = EpicsSignal('depo2:plc:Magnetron_7_Power_RB', \
#     write_pv = 'depo2:plc:Mag7_Pwr_Enable_OUT', \
# )
# relay_magnetron[8] = EpicsSignal('depo2:plc:Magnetron_8_Power_RB', \
#     write_pv = 'depo2:plc:Mag8_Pwr_Enable_OUT', \
# )
# relay_dc_input_2 = EpicsSignal('depo2:plc:DC_Input_2_RB', \
#     'write_pv' = depo2:plc:DC_In_2_Enable_OUT, \
# )
# relay_dc_input_1 = EpicsSignal('depo2:plc:DC_Power_Input_1_RB', \
#     'write_pv' = depo2:plc:DC_Pwr_In_Enable_OUT, \
# )
# relay_spare_input_1 = EpicsSignal('depo2:plc:Spare_Input_1_RB', \
#     'write_pv' = depo2:plc:Spare_In_1_Enable_OUT, \
# )DepositionListDevice
# relay_spare_input_2 = EpicsSignal('depo2:plc:Spare_Input_2_RB', \
#     'write_pv' = depo2:plc:Spare_In_2_Enable_OUT, \
# )
# relay_spare_power_a = EpicsSignal('depo2:plc:Spare_Power_A_RB', \
#     'write_pv' = depo2:plc:Spare_Pwr_A_Enable_OUT, \
# )
# relay_spare_power_b = EpicsSignal('depo2:plc:Spare_Power_B_RB', \
#     'write_pv' = depo2:plc:Spare_Pwr_B_Enable_OUT, \
# )
# relay_spare_power_c = EpicsSignal('depo2:plc:Spare_Power_C_RB', \
#     'write_pv' = depo2:plc:Spare_Pwr_C_Enable_OUT, \
# )
# relay_spare_power_d = EpicsSignal('depo2:plc:Spare_Power_D_RB', \
#     'write_pv' = depo2:plc:Spare_Pwr_D_Enable_OUT, \
# )
# ps1_current_raw = EpicsSignal('depo2:plc:Iout_1_IN', \
#     'write_pv' = depo2:plc:Sputter_PS1_Cur_OUT, \
# )
# ps2_current_raw = EpicsSignal('depo2:plc:Iout_2_IN', \
#     'write_pv' = depo2:plc:Sputter_PS2_Cur_OUT, \
# )
# ps1_power_raw = EpicsSignal('depo2:plc:Pout_1_IN', \
#     'write_pv' = depo2:plc:Sputter_PS1_Pwr_OUT, \
# )
# ps2_power_raw = EpicsSignal('depo2:plc:Pout_2_IN', \
#     'write_pv' = depo2:plc:Sputter_PS2_Pwr_OUT, \
# )
# ps1_volts_avg =DepositionListDevice EpicsSignal('depo2:userAve9.VAL')
# ps2_voltage_raw = EpicsSignal('depo2:plc:Vout_2_IN')
# ps1_power = EpicsSignal('depo2:userCalc9', \
#     'write_pv' = depo2:userCalc6.A, \
# )
# ps1_current = EpicsSignal('depo2:userCalc10', \
#     'write_pv' = depo2:userCalc7.A, \
# )
# ps1_voltage = EpicsSignal('depo2:userCalc8', \
#     'write_pv' = depo2:userCalc5.A, \
# )
# mps1_indicator = EpicsSignal('depo2:plc:MPS1_Mag_Ind_IN')
# mps1_status = EpicsSignal('depo2:plc:MPS1_Mag_Status_IN')
# mps2_indicator = EpicsSignal('depo2:plc:MPS2_Mag_Ind_IN')
# mps2_status = EpicsSignal('depo2:plc:MPS2_Mag_Status_IN')
# mps1_plc_fault = EpicsSignal('depo2:plc:MPS1_Magnetron_Fault_IN')
# mps2_plc_fault = EpicsSignal('depo2:plc:MPS2_Magnetron_Fault_IN')
# mps1_power_on = EpicsSignal('depo2:plc:MPS1_Magnetron_Power_RB', \
#     'write_pv' = depo2:plc:MPS1_Mag_Pwr_On_OUT, \
# )
# mps1_enable_output_plc = EpicsSignal('depo2:plc:MPS1_PS_Enable_OUT')
# mps1_remote_enable = EpicsSignal('depo2:plc:MPS1_Remote_Enable_OUT')
# mps2_power_on = EpicsSignal('depo2:plc:MPS2_Magnetron_Power_RB', \
#     'write_pv' DepositionListDevice= depo2:plc:MPS2_Mag_Pwr_On_OUT, \
# )
# mps2_enable_output = EpicsSignal('depo2:plc:MPS2_PS_Enable_OUT')
# mps2_remote_enable = EpicsSignal('depo2:plc:MPS2_Remote_Enable_OUT')
# mps1_rs232_control_status = EpicsSignalRO('depo2:ION:1:rs232_status')
# mps1_rs232_disable_control = EpicsSignal('depo2:ION:1:set_analog_ctl.PROC')
# mps1_rs232_enable_control = EpicsSignal('depo2:ION:1:set_rs232_ctl.PROC')
# mps1_disable_output = EpicsSignal('depo2:ION:1:set_disable.PROC')
# mps1_enable_output = EpicsSignal('depo2:ION:1:set_enable.PROC')
# EpicsSignalRO('depo2:ION:1:out_status')
# mps1_fault_interlock = EpicsSignalRO('depo2:ION:1:intlk')
# mps1_fault_bus = EpicsSignalRO('depo2:ION:1:busflt')
# mps1_fault_line = EpicsSignalRO('depo2:ION:1:lineflt')
# mps1_fault_thermal = EpicsSignalRO('depo2:ION:1:thermflt')
# mps1_fault_overtemp = EpicsSignalRO('depo2:ION:1:overTflt')
# mps1_fault_heartbeat = EpicsSignalRO('depo2:ION:1:hbflt')
# EpicsSignal('depo2:ION:1:read_all.SCAN')
# mps1_power_rbv = EpicsSignalRO('depo2:ION:1:watts_rd')
# mps1_current_rbv = EpicsSignalRO('depo2:ION:1:amps_rd')
# mps1_voltage_rbv = EpicsSignalRO('depo2:ION:1:volts_rd')
# mps1_arc_rate = EpicsSignalRO('depo2:ION:1:arc_rate_rd')
# depo2:ION:1:target_rd('EpicsSignal', 'write_pv' = depo2:ION:1:target, \
# )
# mps1_heartbeat = EpicsSignal('depo2:ION:1:hb_timeout_rd', \
#     'write_pv' DepositionListDevice= depo2:ION:1:heartbeat, \
# )
# mps1_power = EpicsSignal('depo2:ION:1:target_power_sp_rd', \
#     'write_pv' = depo2:ION:1:power, \
# )
# mps1_current = EpicsSignal('depo2:ION:1:target_current_sp_rd', \
#     'write_pv' = depo2:ION:1:current, \
# )
# mps1_voltage = EpicsSignal('depo2:ION:1:target_voltage_sp_rd', \
#     'write_pv' = depo2:ION:1:voltage, \
# )
# mps1_arc_detect_delay = EpicsSignal('depo2:ION:1:target_dly_time_rd', \
#     'write_pv' = depo2:ION:1:arc_detect_delay, \
# )
# mps1_arc_off_time = EpicsSignal('depo2:ION:1:target_off_time_rd', \
#     'write_pv' = depo2:ION:1:arc_off_time, \
# )
# mps1_kwh_limit = EpicsSignal('depo2:ION:1:mps1_kwh_limit', \
#     'write_pv' = depo2:ION:1:kwh_limit, \
# )
# mps1_kwh_count_reset = EpicsSignal('depo2:ION:1:target_ramp_time_rd', \
#     'write_pv' = depo2:ION:1:reset_kwh_count.PROC, \
# )
# mps1_ramp_time = EpicsSignal('depo2:ION:1:target_ramp_time_rd', \
#     'write_pv' = depo2:ION:1:ramp_time, \
# )
# mps1_run_time = EpicsSignal('depo2:ION:1:target_run_time_rd', \
#     'write_pv' = depo2:ION:1:run_time, \
# )DepositionListDevice
# gun_select = EpicsSignal('depo2:userCalcOut10.A', \
#     'write_pv' = depo2:userCalcOut10.A, \
# )
# gun_voltage = {}
# gun_voltage_avg[1] = EpicsSignalRO('depo2:userAve1.VAL')
# gun_voltage_avg[2] = EpicsSignalRO('depo2:userAve2.VAL')
# gun_voltage_avg[3] = EpicsSignalRO('depo2:userAve3.VAL')
# gun_voltage_avg[4] = EpicsSignalRO('depo2:userAve4.VAL')
# gun_voltage_avg[5] = EpicsSignalRO('depo2:userAve5.VAL')
# gun_voltage_avg[6] = EpicsSignalRO('depo2:userAve6.VAL')
# gun_voltage_avg[7] = EpicsSignalRO('depo2:userAve7.VAL')
# gun_voltage_avg[8] = EpicsSignalRO('depo2:userAve8.VAL')
# baratron_pressure = EpicsSignal('depo2:plc:PT_1_IN', \
#     'write_pv' = depo2:plc:PT_1_OUT, \
# )
# main_chamber_1000t_pressure = EpicsSignal('depo2:plc:PT_2_IN')
# loadlock_chamber_10t_pressure = EpicsSignal('depo2:plc:PT_3_IN')
# loadlock_1000t_pressure = EpicsSignal('depo2:plc:PT_4_IN')
# cp1_pressure = EpicsSignal('depo2:plc:PT_5_IN')
# cp2_pressure = EpicsSignal('depo2:plc:PT_6_IN')
# cp3_pressure = EpicsSignal('depo2:plc:PT_7_IN')
# cp4_pressure = EpicsSignal('depo2:plc:PT_8_IN')
# vfd1_speed = EpDepositionListDeviceicsSignal('depo2:plc:VFD_1_IN', \
#     'write_pv' = depo2:plc:VFD_1_OUT, \
# )
# AC_Phase_Fail_IN = EpicsSignal('depo2:plc:AC_Phase_Fail_IN')
# ACphase_Failure_IN = EpicsSignal('depo2:plc:ACphase_Failure_IN')
# Alarm_Reset_Sw_IN = EpicsSignal('depo2:plc:Alarm_Reset_Sw_IN', \
#     'write_pv' = depo2:plc:Alarm_Reset_OUT, \
# )
# alarm_silence_door_switch = EpicsSignal('depo2:plc:Alarm_Silence_Sw_IN')
# alarm_silence = EpicsSignal('depo2:plc:Alarm_Silence_RB', \
#     'write_pv' = depo2:plc:Alarm_Silence_RB, \
# )
# Argon_Press_Sw_IN = EpicsSignal('depo2:plc:Argon_Press_Sw_IN')
# Argon_Pressure_Alarm_IN = EpicsSignal('depo2:plc:Argon_Pressure_Alarm_IN')
# Cabinet_Doors_Sw_IN = EpicsSignal('depo2:plc:Cabinet_Doors_Sw_IN')
# hs_cart_at_umbilical_pos = EpicsSignal('depo2:plc:Cart_at_ConnDis_Pos_IN')
# Cart_at_Home_Pos_IN = EpicsSignal('depo2:plc:Cart_at_Home_Pos_IN')
# Cart_at_Landing_Pos_IN = EpicsSignal('depo2:plc:Cart_at_Landing_Pos_IN')
# cart_fully_on_loadplate = EpicsSignal('depo2:plc:Cart_at_LoadLock1_Pos_IN')
# hs_extractor_at_main_rail = EpicsSignal('depo2:plc:Cart_at_LoadLock2_Pos_IN')
# hs_extractor_away_from_gv5 = EpicsSignal('depo2:plc:Cart_at_LoadLock3_Pos_IN')
# Cart_at_LoadLock_Pos_IN = EpicsSignal('depo2:plc:Cart_at_LoadLock_Pos_IN')
# cp1_temp_status = EpicsSignal('depo2:plc:Cryo_Pump_1_ok_IN')
# cp2_temp_status = EpicsSignal('depo2:plc:Cryo_Pump_2_ok_IN')
# cp3_temp_status = EpicsSignal('depo2:plc:Cryo_Pump_3_ok_IN')
# cp4_temp_status = EpicsSignal('depo2:plc:Cryo_Pump_4_ok_IN')
# Customer_Facility_Abort_IN = EpicsSignal('depo2:plc:Customer_Facility_Abort_IN')
# gundoor_vfd_status = EpicsSignal('depo2:plc:GunDoor_VFD_ok_IN')
# lmc_plc_b0_inpuDepositionListDevicet = EpicsSignal('depo2:plc:LMC_PLC_B0_IN')
# lmc_plc_b1_input = EpicsSignal('depo2:plc:LMC_PLC_B1_IN')
# lmc_plc_b2_input = EpicsSignal('depo2:plc:LMC_PLC_B2_IN')
# lmc_plc_b3_input = EpicsSignal('depo2:plc:LMC_PLC_B3_IN')
# sensor_loadlock_door = EpicsSignal('depo2:plc:LoadLock_Door_Not_Closed_IN')
# Vac_Pump_T_ok_IN = EpicsSignal('depo2:plc:Vac_Pump_T_ok_IN')
# Vac_Pump_VFD_ok_IN = EpicsSignal('depo2:plc:Vac_Pump_VFD_ok_IN')
# C472_IN = EpicsSignal('depo2:plc:C472_IN')
# C474_IN = EpicsSignal('depo2:plc:C474_IN')
# plug_moving = EpicsSignalRO('depo2:plc:C512_IN')
# plug_engaged_limit = EpicsSignalRO('depo2:plc:C513_IN')
# plug_disengaged_limit = EpicsSignalRO('depo2:plc:C514_IN')
# plug_direction = EpicsSignalRO('depo2:plc:C515_IN')
# C516_IN = EpicsSignal('depo2:plc:C516_IN')
# C517_IN = EpicsSignal('depo2:plc:C517_IN')
# Customer_Abort_IN = EpicsSignal('depo2:plc:Customer_Abort_IN')
# DI1_D7_IN = EpicsSignal('depo2:plc:DI1_D7_IN')
# DI2_B6_IN = EpicsSignal('depo2:plc:DI2_B6_IN')
# DI2_B7_IN = EpicsSignal('depo2:plc:DI2_B7_IN')
# DI2_C0_IN = EpicsSignal('depo2:plc:DI2_C0_IN')
# DI2_C1_IN = EpicsSignal('depo2:plc:DI2_C1_IN')
# DI2_C2_IN = EpicsSignal('depo2:plc:DI2_C2_IN')
# DI2_C3_IN = EpicsSignal('depo2:plc:DI2_C3_IN')
# DI2_C4_IN = EpicsSignal('depo2:plc:DI2_C4_IN')
# DI2_C5_IN = EpicsSignal('depo2:plc:DI2_C5_IN')
# DI2_C6_IN = EpicsSignal('depo2:plc:DI2_C6_IN')
# DI2_C7_IN = EpicsSignal('depo2:plc:DI2_C7_IN')
# DI2_D0_IN = EpicsSignal('depo2:plc:DI2_D0_IN')
# DI2_D1_IN = EpicsSignal('depo2:plc:DI2_D1_IN')
# DI2_D2_IN = EpicsSignal('depo2:plc:DI2_D2_IN')
# DI2_D3_IN = EpicsSignal('depo2:plc:DI2_D3_IN')
# DI2_D4_IN = EpicsSignal('depo2:plc:DI2_D4_IN')
# DI2_D5_IN = EpicsSignal('depo2:plc:DI2_D5_IN')
# DI2_D6_IN = EpicsSignal('depo2:plc:DI2_D6_IN')
# DI2_D7_IN = EpicsSignal('depo2:plc:DI2_D7_IN')
# Failed_Hazards_IN = EpicsSignal('depo2:plc:Failed_Hazards_IN')
# Gun_Door_Motor_Alarm_IN = EpicsSignal('depo2:plc:Gun_Door_Motor_Alarm_IN')
# Hazards_IN = EpicsSignal('depo2:plc:Hazards_IN')
# Injects_Interrupted_IN = EpicsSignal('depo2:plc:Injects_Interrupted_IN')
# Loadlock_Over_Pressure_IN = EpicsSignal('depo2:plc:Loadlock_Over_Pressure_IN')
# Motion_Status_IN = EpicsSignal('depo2:plc:Motion_Status_IN')
# Nitrogen_Press_Sw_IN = EpicsSignal('depo2:plc:Nitrogen_Press_Sw_IN')
# Nitrogen_Pressure_Alarm_IN = EpicsSignal('depo2:plc:Nitrogen_Pressure_Alarm_IN')
# Pneumatic_Press_Sw_IN = EpicsSignal('depo2:plc:Pneumatic_Press_Sw_IN')
# Pneumatic_Pressure_Alarm_IN = EpicsSignal('depo2:plc:Pneumatic_Pressure_Alarm_IN')
# Process_Alert_IN = EpicsSignal('depo2:plc:Process_Alert_IN')
# Process_Tube_IN = EpicsSignal('depo2:plc:Process_Tube_IN')
# Ready_To_Transfer_IN = EpicsSignal('depo2:plc:Ready_To_Transfer_IN')
# Seals_Leak_Alarm_IN = EpicsSignal('depo2:plc:Seals_Leak_Alarm_IN')
# Seals_Vac_Sw_IN = EpicsSignal('depo2:plc:Seals_Vac_Sw_IN')
# System_Warning_IN = EpicsSignal('depo2:plc:System_Warning_IN')
# Totalizing_Purge_Cond_IN = EpicsSignal('depo2:plc:Totalizing_Purge_Cond_IN')
# Totalizing_Purge_Flow_IN = EpicsSignal('depo2:plc:Totalizing_Purge_Flow_IN')
# Vacuum_Pump_Alarm_IN = EpicsSignal('depo2:plc:Vacuum_Pump_Alarm_IN')
# Vacuum_Pump_Overtemp_IN = EpicsSignal('depo2:plc:Vacuum_Pump_Overtemp_IN')
# Watchdog_Alarm_IN = EpicsSignal('depo2:plc:Watchdog_Alarm_IN')
# Watchdog_Status_IN = EpicsSignal('depo2:plc:Watchdog_Status_IN')
# Watchdog_Timer_Alarm_IN = EpicsSignal('depo2:plc:Watchdog_Timer_Alarm_IN')
# water_flow_meter_in = EpicsSignal('depo2:plc:WFM_1_IN')
# Cooling_Water_Flow_IN = EpicsSignal('depo2:plc:Cooling_Water_Flow_IN')
# Water_Flow_Sw_IN = EpicsSignal('depo2:plc:Water_Flow_Sw_IN')
# water_flow_cathode_1UC = EpicsSignalRO('depo2:userCalcOut11.VAL')
# water_flow_cathode_2UC = EpicsSignalRO('depo2:userCalcOut12.VAL')
# water_flow_cathode_3UC = EpicsSignalRO('depo2:userCalcOut13.VAL')
# water_flow_cathode_4UC = EpicsSignalRO('depo2:userCalcOut14.VAL')
# water_flow_cathode_5UC = EpicsSignalRO('depo2:userCalcOut15.VAL')
# water_flow_cathode_6UC = EpicsSignalRO('depo2:userCalcOut16.VAL')
# water_flow_cathode_7UC = EpicsSignalRO('depo2:userCalcOut17.VAL')
# water_flow_cathode_8UC = EpicsSignalRO('depo2:userCalcOut18.VAL')
# Abort_Indicator_RB = EpicsSignal('depo2:plc:Abort_Indicator_RB', \
#     'write_pv' = depo2:plc:Abort_Indicator_OUT, \
# )
# Argon_Purge_Out_RB = EpicsSignal('depo2:plc:Argon_Purge_Out_RB', \
#     'write_pv' = depo2:plc:Argon_Purge_On_OUT, \
# )
# Audible_Alert_RB = EpicsSignal('depo2:plc:Audible_Alert_RB')
# cc_exhaust_to_vp1 = EpicsSignal('depo2:plc:CC_Exhaust_to_VP1_RB', \
#     'write_pv' = depo2:plc:CC_Exhaust_VP1_On_OUT, \
# )
# cp1_exhaust_to_vp1 = EpicsSignal('depo2:plc:CP1_Exhaust_to_VP1_RB', \
#     'write_pv' = depo2:plc:CP1_Exhaust_VP1_On_OUT, \
# )
# cp1_on = EpicsSignal('depo2:plc:CP1_Landing_Chamber_Cryo_Pump_RB', \
#     'write_pv' = depo2:plc:CP1_LC_Cryo_Pump_Off_OUT, \
# )
# cp2_exhaust_to_vp1 = EpicsSignal('depo2:plc:CP2_Exhaust_to_VP1_RB', \
#     'write_pv' = depo2:plc:CP2_Exhaust_VP1_On_OUT, \
# )
# cp2_on = EpicsSignal('depo2:plc:CP2_Planar_Chamber_Cryo_Pump_RB', \
#     'write_pv' = depo2:plc:CP2_PC_Cryo_Pump_Off_OUT, \
# )
# cp3_exhaust_to_vp1 = EpicsSignal('depo2:plc:CP3_Exhaust_to_VP1_RB', \
#     'write_pv' = depo2:plc:CP3_Exhaust_VP1_On_OUT, \
# )
# cp3_on = EpicsSignal('depo2:plc:CP3_Round_Chamber_Cryo_Pump_RB', \
#     'write_pv' = depo2:plc:CP3_RC_Cryo_Pump_Off_OUT, \
# )
# cp4_exhaust_to_vp1 = EpicsSignal('depo2:plc:CP4_Exhaust_to_VP1_RB', \
#     'write_pv' = depo2:plc:CP4_Exhaust_VP1_On_OUT, \
# )
# cp4_on = EpicsSignal('depo2:plc:CP4_Loadlock_Chamber_Cryo_Pump_RB', \
#     'write_pv' = depo2:plc:CP4_LLC_Cryo_Pump_Off_OUT, \
# )
# Center_Chamber_Overpressure_RB = EpicsSignal('depo2:plc:Center_Chamber_Overpressure_RB', \
#     'write_pv' = depo2:plc:CC_OverPress_Close_OUT, \
# )
# av17 = EpicsSignal('depo2:plc:AV17_RB', \
#     'write_pv' = depo2:plc:AV17, \
# )
# im_av_lfn = EpicsSignal('depo2:plc:AV26_RB', \
#     'write_pv' = depo2:plc:AV26, \
# )
# av27 = EpicsSignal('depo2:plc:AV27_RB', \
#     'write_pv' = depo2:plc:AV27, \
# )
# av30 = EpicsSignal('depo2:plc:AV30_RB', \
#     'write_pv' = depo2:plc:AV30, \
# )
# av31 = EpicsSignal('depo2:plc:AV31_RB', \
#     'write_pv' = depo2:plc:AV31, \
# )
# av32 = EpicsSignal('depo2:plc:AV32_RB', \
#     'write_pv' = depo2:plc:AV32, \
# )
# DO2_B0_RB = EpicsSignal('depo2:plc:DO2_B0_RB')
# DO2_D5_RB = EpicsSignal('depo2:plc:DO2_D5_RB')
# eov1_vp2_seals_pump = EpicsSignal('depo2:plc:EOV1_VP2_Seals_Pump_RB', \
#     'write_pv' = depo2:plc:VP2_Seals_Pump_On_OUT, \
# )
# backfill_ll_hi = EpicsSignal('depo2:plc:EOV3_Process_Argon_Hi_Backfill_RB', \
#     'write_pv' = depo2:plc:LL_Ar_Hi_Bf_On_OUT, \
# )
# backfill_main_hi = EpicsSignal('depo2:plc:EOV2_Loadlock_Argon_Hi_Backfill_RB', \
#     'write_pv' = depo2:plc:Process_Ar_Hi_Bf_On_OUT, \
# )
# backfill_main_lo = EpicsSignal('depo2:plc:Ar_Backfill_to_Center_RB', \
#     'write_pv' = depo2:plc:Ar_Backfill_CC_On_OUT, \
# )
# backfill_ll_lo = EpicsSignal('depo2:plc:Ar_Backfill_to_LL_RB', \
#     'write_pv' = depo2:plc:Ar_Backfill_LL_On_OUT, \
# )
# eov4_loadlock_door_seal = EpicsSignal('depo2:plc:EOV4_Loadlock_Door_Seal_RB', \
#     'write_pv' = depo2:plc:LL_Door_Seal_Open_OUT, \
# )
# n2_purge_vp1 = EpicsSignal('depo2:plc:EOV5_N2_Purge_to_VP1_RB', \
#     'write_pv' = depo2:plc:N2_Purge_VP1_Open_OUT, \
# )
# extractor_motor_clutch = EpicsSignal('depo2:plc:Extractor_Motor_Clutch_RB', \
#     'write_pv' = depo2:plc:LL_Ext_Motor_Clutch_On_OUT, \
# )
# grabber_motor_clutch = EpicsSignal('depo2:plc:Grabber_Motor_Clutch_RB', \
#     'write_pv' = depo2:plc:Grabber_Motor_Clutch_On_OUT, \
# )
# grabber_motor_enable = EpicsSignal('depo2:plc:Grabber_Motor_Enable_RB', \
#     'write_pv' = depo2:plc:Grabber_Motor_Enable_OUT, \
# )
# grabber_motor_away_from_chamber = EpicsSignal('depo2:plc:Grabber_Motor_Forward_RB', \
#     'write_pv' = depo2:plc:Grabber_Motor_Fwd_On_OUT, \
# )
# grabber_motor_into_chamber = EpicsSignal('depo2:plc:Grabber_Motor_Reverse_RB', \
#     'write_pv' = depo2:plc:Grabber_Motor_Rev_On_OUT, \
# )
# LMC_PLC_Handshake_B0_RB = EpicsSignal('depo2:plc:LMC_PLC_Handshake_B0_RB')
# LMC_PLC_Handshake_B1_RB = EpicsSignal('depo2:plc:LMC_PLC_Handshake_B1_RB')
# LMC_PLC_Handshake_B2_RB = EpicsSignal('depo2:plc:LMC_PLC_Handshake_B2_RB')
# ccg1_power_on = EpicsSignal('depo2:plc:Landing_Chamber_CCG1_RB', \
#     'write_pv' = depo2:plc:LC_CCG1_Enable_OUT, \
# )
# linear_motor_amp_enabled = EpicsSignal('depo2:plc:Linear_Motor_Power_Amp_RB', \
#     'write_pv' = depo2:plc:Linear_Motor_Pwr_On_OUT, \
# )
# ccg2_power_on = EpicsSignal('depo2:plc:Loadlock_CCG2_RB', \
#     'write_pv' = depo2:plc:LL_CCG2_Enable_OUT, \
# )
# ccg1_pressure = EpicsSignal('depo2:plc:CCG_1_IN')
# ccg2_pressure = EpicsSignal('depo2:plc:CCG_2_IN')
# Loadlock_Extended_Position_RB = EpicsSignal('depo2:plc:Loadlock_Extended_Position_RB')
# Loadlock_Extract_Motor_Direction_RB = EpicsSignal('depo2:plc:Loadlock_Extract_Motor_Direction_RB')
# loadlock_extractor_motor_enable = EpicsSignal('depo2:plc:Loadlock_Extract_Motor_Enable_RB', \
#     'write_pv' = depo2:plc:LL_Ext_Motor_Enable_OUT, \
# )
# loadlock_extractor_out = EpicsSignal('depo2:plc:Loadlock_Extractor_Forward_RB', \
#     'write_pv' = depo2:plc:LL_Ext_Motor_Fwd_On_OUT, \
# )
# loadlock_extractor_in = EpicsSignal('depo2:plc:Loadlock_Extractor_Reverse_RB', \
#     'write_pv' = depo2:plc:LL_Ext_Motor_Rev_On_OUT, \
# )
# loadlock_overpressure_valve = EpicsSignal('depo2:plc:Loadlock_Overpressure_RB', \
#     'write_pv' = depo2:plc:LL_OverPress_Close_OUT, \
# )
# loadlock_to_vp1 = EpicsSignal('depo2:plc:Loadlock_to_VP1_RB', \
#     'write_pv' = depo2:plc:LL_VP1_On_OUT, \
# )
# mfc1_valve_on = EpicsSignal('depo2:plc:MFC1_RB', \
#     'write_pv' = depo2:plc:MFC1_RC_On_OUT, \
# )
# mfc1_plc_bypass = EpicsSignal('depo2:plc:MFC1_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC1_Manual_OUT, \
# )
# mfc2_valve_on = EpicsSignal('depo2:plc:MFC2_RB', \
#     'write_pv' = depo2:plc:MFC2_RC_On_OUT, \
# )
# mfc2_plc_bypass = EpicsSignal('depo2:plc:MFC2_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC2_Manual_OUT, \
# )
# mfc3_valve_on = EpicsSignal('depo2:plc:MFC3_RB', \
#     'write_pv' = depo2:plc:MFC3_RC_On_OUT, \
# )
# mfc3_plc_bypass = EpicsSignal('depo2:plc:MFC3_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC3_Manual_OUT, \
# )
# mfc4_valve_on = EpicsSignal('depo2:plc:MFC4_RB', \
#     'write_pv' = depo2:plc:MFC4_RC_On_OUT, \
# )
# mfc4_plc_bypass = EpicsSignal('depo2:plc:MFC4_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC4_Manual_OUT, \
# )
# mfc5_valve_on = EpicsSignal('depo2:plc:MFC5_RB', \
#     'write_pv' = depo2:plc:MFC5_RC_On_OUT, \
# )
# mfc5_plc_bypass = EpicsSignal('depo2:plc:MFC5_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC5_Manual_OUT, \
# )
# mfc6_valve_on = EpicsSignal('depo2:plc:MFC6_RB', \
#     'write_pv' = depo2:plc:MFC6_RC_On_OUT, \
# )
# mfc6_plc_bypass = EpicsSignal('depo2:plc:MFC6_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC6_Manual_OUT, \
# )
# mfc7_valve_on = EpicsSignal('depo2:plc:MFC7_RB', \
#     'write_pv' = depo2:plc:MFC7_RC_On_OUT, \
# )
# mfc7_plc_bypass = EpicsSignal('depo2:plc:MFC7_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC7_Manual_OUT, \
# )
# mfc8_valve_on = EpicsSignal('depo2:plc:MFC8_RB', \
#     'write_pv' = depo2:plc:MFC8_RC_On_OUT, \
# )
# mfc8_plc_bypass = EpicsSignal('depo2:plc:MFC8_Manual_OUT', \
#     'write_pv' = depo2:plc:MFC8_Manual_OUT, \
# )
# mfc1_flow = EpicsSignal('depo2:plc:MFC_1_IN', \
#     'write_pv' = depo2:plc:MFC_1_OUT, \
# )
# mfc2_flow = EpicsSignal('depo2:plc:MFC_2_IN', \
#     'write_pv' = depo2:plc:MFC_2_OUT, \
# )
# mfc3_flow = EpicsSignal('depo2:plc:MFC_3_IN', \
#     'write_pv' = depo2:plc:MFC_3_OUT, \
# )
# mfc4_flow = EpicsSignal('depo2:plc:MFC_4_IN', \
#     'write_pv' = depo2:plc:MFC_4_OUT, \
# )
# mfc5_flow = EpicsSignal('depo2:plc:MFC_5_IN', \
#     'write_pv' = depo2:plc:MFC_5_OUT, \
# )
# mfc6_flow = EpicsSignal('depo2:plc:MFC_6_IN', \
#     'write_pv' = depo2:plc:MFC_6_OUT, \
# )
# mfc7_flow = EpicsSignal('depo2:plc:MFC_7_IN', \
#     'write_pv' = depo2:plc:MFC_7_OUT, \
# )
# mfc8_flow = EpicsSignal('depo2:plc:MFC_8_IN', \
#     'write_pv' = depo2:plc:MFC_8_OUT, \
# )
# mfc1_epics_pid_control = EpicsSignal('depo2:userCalc1.A', \
#     'write_pv' = depo2:userCalc1.A, \
# )
# mfc2_epics_pid_control = EpicsSignal('depo2:userCalc1.B', \
#     'write_pv' = depo2:userCalc1.B, \
# )
# mfc3_epics_pid_control = EpicsSignal('depo2:userCalc1.C', \
#     'write_pv' = depo2:userCalc1.C, \
# )
# mfc4_epics_pid_control = EpicsSignal('depo2:userCalc1.D', \
#     'write_pv' = depo2:userCalc1.D, \
# )
# mfc5_epics_pid_control = EpicsSignal('depo2:userCalc1.E', \
#     'write_pv' = depo2:userCalc1.E, \
# )
# mfc6_epics_pid_control = EpicsSignal('depo2:userCalc1.F', \
#     'write_pv' = depo2:userCalc1.F, \
# )
# mfc7_epics_pid_control = EpicsSignal('depo2:userCalc1.G', \
#     'write_pv' = depo2:userCalc1.G, \
# )
# mfc8_epics_pid_control = EpicsSignal('depo2:userCalc1.H', \
#     'write_pv' = depo2:userCalc1.H, \
# )
# magnetron_door_motor_enabled = EpicsSignal('depo2:plc:Magnetron_Door_Motor_RB', \
#     'write_pv' = depo2:plc:Mag_Door_Motor_Enable_OUT, \
# )
# n2_purge_cp1 = EpicsSignal('depo2:plc:N2_Purge_to_CP1_RB', \
#     'write_pv' = depo2:plc:N2_Purge_CP1_OUT, \
# )
# n2_purge_cp2 = EpicsSignal('depo2:plc:N2_Purge_to_CP2_RB', \
#     'write_pv' = depo2:plc:N2_Purge_CP2_OUT, \
# )
# n2_purge_cp3 = EpicsSignal('depo2:plc:N2_Purge_to_CP3_RB', \
#     'write_pv' = depo2:plc:N2_Purge_CP3_OUT, \
# )
# n2_purge_cp4 = EpicsSignal('depo2:plc:N2_Purge_to_CP4_RB', \
#     'write_pv' = depo2:plc:N2_Purge_CP4_OUT, \
# )
# pt1_to_process_chamber = EpicsSignal('depo2:plc:PT1_RB', \
#     'write_pv' = depo2:plc:PT1_LC_On_OUT, \
# )
# gv1_position = EpicsSignal('depo2:plc:GV_1_Pos_IN', \
#     'write_pv' = depo2:plc:GV_1_Pos_OUT, \
# )
# gv2_position = EpicsSignal('depo2:plc:GV_2_Pos_IN', \
#     'write_pv' = depo2:plc:GV_2_Pos_OUT, \
# )
# gv3_position = EpicsSignal('depo2:plc:GV_3_Pos_IN', \
#     'write_pv' = depo2:plc:GV_3_Pos_OUT, \
# )
# gv4_position = EpicsSignal('depo2:plc:GV_4_Pos_IN', \
#     'write_pv' = depo2:plc:GV_4_Pos_OUT, \
# )
# gv5_closed_status = EpicsSignalRO('depo2:plc:LL_GV5_Closed_IN')
# gv5_open_status = EpicsSignalRO('depo2:plc:LL_GV5_Open_IN')
# gv5_close_request = EpicsSignal('depo2:plc:Loadlock_GV5_Closed_RB', \
#     'write_pv' = depo2:plc:LL_GV5_Close_OUT, \
# )
# gv5_open_request = EpicsSignal('depo2:plc:Loadlock_GV5_Open_RB', \
#     'write_pv' = depo2:plc:LL_GV5_Open_OUT, \
# )
# gv1_close_request = EpicsSignal('depo2:plc:Landing_Chamber_Cryo_GV1_CLOSED_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV1_Close_OUT, \
# )
# gv1_open_request = EpicsSignal('depo2:plc:Landing_Chamber_Cryo_GV1_OPEN_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV1_Open_OUT, \
# )
# gv1_fully_closed = EpicsSignalRO('depo2:plc:LC_GV1_DoorClosed_IN')
# gv1_fully_open = EpicsSignalRO('depo2:plc:LC_GV1_DoorOpen_IN')
# gv2_close_request = EpicsSignal('depo2:plc:Planar_Chamber_Cryo_GV2_CLOSED_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV2_Close_OUT, \
# )
# gv2_open_request = EpicsSignal('depo2:plc:Planar_Chamber_Cryo_GV2_OPEN_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV2_Open_OUT, \
# )
# gv2_fully_closed = EpicsSignalRO('depo2:plc:RC_GV2_Closed_IN')
# gv2_fully_open = EpicsSignalRO('depo2:plc:RC_GV2_Open_IN')
# gv3_close_request = EpicsSignal('depo2:plc:Round_Chamber_Cryo_GV3_CLOSED_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV3_Close_OUT, \
# )
# gv3_open_request = EpicsSignal('depo2:plc:Round_Chamber_Cryo_GV3_OPEN_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV3_Open_OUT, \
# )
# gv3_fully_closed = EpicsSignalRO('depo2:plc:PC_GV3_Closed_IN')
# gv3_fully_open = EpicsSignalRO('depo2:plc:PC_GV3_Open_IN')
# gv4_close_request = EpicsSignal('depo2:plc:Loadlock_Chamber_Cryo_GV4_CLOSED_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV4_Close_OUT, \
# )
# gv4_open_request = EpicsSignal('depo2:plc:Loadlock_Chamber_Cryo_GV4_OPEN_RB', \
#     'write_pv' = depo2:plc:LC_Cryo_GV4_Open_OUT, \
# )
# gv4_fully_closed = EpicsSignalRO('depo2:plc:LL_GV4_Closed_IN')
# gv4_fully_open = EpicsSignalRO('depo2:plc:LL_GV4_Open_IN')
# planar_magnetron_door_select = EpicsSignal('depo2:plc:Planar_Door_Motor_RB', \
#     'write_pv' = depo2:plc:Planar_Door_Motor_Enable_OUT, \
# )
# round_magnetron_door_select = EpicsSignal('depo2:plc:Round_Door_Motor_RB', \
#     'write_pv' = depo2:plc:Round_Door_Motor_Enable_OUT, \
# )
# VP1_Process_Vacuum_Pump_RB = EpicsSignal('depo2:plc:VP1_Process_Vacuum_Pump_RB', \
#     'write_pv' = depo2:plc:VP1_Vac_Pump_On_OUT, \
# )
# Watchdog_Reset_Pulse_RB = EpicsSignal('depo2:plc:Watchdog_Reset_Pulse_RB')
# plug_disconnect = EpicsSignal('depo2:plc:Unload_Cart_Request_OUT', \
#     'write_pv' = depo2:plc:Unload_Cart_Request_OUT, \
# )
# test_run_cart = EpicsSignal('depo2:plc:Run_Cart_OUT', \
#     'write_pv' = depo2:plc:Run_Cart_OUT, \
# )
# test_home_cart = EpicsSignal('depo2:plc:Home_Cart_OUT', \
#     'write_pv' = depo2:plc:Home_Cart_OUT, \
# )
# plug_after_connect = EpicsSignal('depo2:plc:Load_Cart_Request_OUT', \
#     'write_pv' = depo2:plc:Load_Cart_Request_OUT, \
# )
# plug_connect = EpicsSignal('depo2:plc:Load_Seq_Stop_OUT', \
#     'write_pv' = depo2:plc:Load_Seq_Stop_OUT, \
# )
# pid1_setpoint = EpicsSignal('depo2:async_pid_slow1.VAL')
# pid1_p = EpicsSignal('depo2:userCalc2.A')
# pid1_i = EpicsSignal('depo2:userCalc3.A')
# pid1_d = EpicsSignal('depo2:userCalc4.A')
# pid1_fbon = EpicsSignal('depo2:async_pid_slow1.FBON')
# pid1_error = EpicsSignalRO('depo2:async_pid_slow1.ERR')
# pid1_readback = EpicsSignalRO('depo2:async_pid_slow1.CVAL')
# pid1_p_readback = EpicsSignalRO('depo2:async_pid_slow1.P', \
#     'write_pv' = depo2:async_pid_slow1.KP, \
# )
# pid1_i_readback = EpicsSignalRO('depo2:async_pid_slow1.I', \
#     'write_pv' = depo2:async_pid_slow1.KI, \
# )
# pid1_d_readback = EpicsSignalRO('depo2:async_pid_slow1.D', \
#     'write_pv' = depo2:async_pid_slow1.KD, \
# )
# depo2w_pt1 = EpicsSignalRO('depo2w:USB231:2:Ai1')
# Rtd_1 = EpicsSignalRO('depo2w:USBTAI:1:RTD1')
# Rtd_2 = EpicsSignalRO('depo2w:USBTAI:1:RTD3')
# run_number = EpicsSignal('depo2:userCalcOut20.A', \
#     'write_pv' = depo2:userCalcOut20.A, \
# )
# water_flow_ALL_cathodes = EpicsSignal('depo2:userCalcOut31', \
#     'write_pv' = depo2:userCalcOut31, \
# )
# water_flow_cathode_raw = {}
# water_flow_cathode_raw[1] = EpicsSignalRO('depo2w:USB231:1:Ai1')
# water_flow_cathode_raw[2] = EpicsSignalRO('depo2w:USB231:1:Ai2')
# water_flow_cathode_raw[3] = EpicsSignalRO('depo2w:USB231:1:Ai3')
# water_flow_cathode_raw[4] = EpicsSignalRO('depo2w:USB231:1:Ai4')
# water_flow_cathode_raw[5] = EpicsSignalRO('depo2w:USB231:1:Ai5')
# water_flow_cathode_raw[6] = EpicsSignalRO('depo2w:USB231:1:Ai6')
# water_flow_cathode_raw[7] = EpicsSignalRO('depo2w:USB231:1:Ai7')
# water_flow_cathode_raw[8] = EpicsSignalRO('depo2w:USB231:1:Ai8')
# water_flow_cathode[1] = EpicsSignalRO('depo2w:water_flow_cathode_1')
# water_flow_cathode[2] = EpicsSignalRO('depo2w:water_flow_cathode_2')
# water_flow_cathode[3] = EpicsSignalRO('depo2w:water_flow_cathode_3')
# water_flow_cathode[4] = EpicsSignalRO('depo2w:water_flow_cathode_4')
# water_flow_cathode[5] = EpicsSignalRO('depo2w:water_flow_cathode_5')
# water_flow_cathode[6] = EpicsSignalRO('depo2w:water_flow_cathode_6')
# water_flow_cathode[7] = EpicsSignalRO('depo2w:water_flow_cathode_7')
# water_flow_cathode[8] = EpicsSignalRO('depo2w:water_flow_cathode_8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:1:Ao1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:1:Ao2')
# im_relay_1_LFN = EpicsSignal('depo2w:USB231:1:Bo1')
# im_relay_2_CMDC = EpicsSignal('depo2w:USB231:1:Bo2')
# if_air_bearing_linear = EpicsSignal('depo2w:USB231:1:Bo3')
# if_air_bearing_angular = EpicsSignal('depo2w:USB231:1:Bo4')
# #somealias = UnknownEpicsSignal('depo2w:USB231:1:Bo5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:1:Bo6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:1:Bo7')
# #somealias = UnknownEpicsSignal('depo2w:USB231:1:Bo8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:2:Ai1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:2:Ai2')
# #somealias = UnknownEpicsSignal('depo2w:USB231:2:Ai3')
# gm_mfc_1_flow = EpicsSignal('depo2w:USB231:2:Ai4', \
#     'write_pv' = depo2w:USB231:2:Ao1, \
# )
# #somealias = UnknownEpicsSignal('depo2w:USB231:2:Ai5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:2:Ai6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:2:Ai7')
# gm_mfc_2_flow = EpicsSignal('depo2w:USB231:2:Ai8', \
#     'write_pv' = depo2w:USB231:2:Ao2, \
# )
# gm_relay_8m = EpicsSignal('depo2w:USB231:2:Bo1')
# gm_relay_8a = EpicsSignal('depo2w:USB231:2:Bo2')
# gm_relay_7m = EpicsSignal('depo2w:USB231:2:Bo3')
# gm_relay_7a = EpicsSignal('depo2w:USB231:2:Bo4')
# gm_relay_6m = EpicsSignal('depo2w:USB231:2:Bo5')
# gm_relay_6a = EpicsSignal('depo2w:USB231:2:Bo6')
# gm_relay_5m = EpicsSignal('depo2w:USB231:2:Bo7')
# gm_relay_5a = EpicsSignal('depo2w:USB231:2:Bo8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai2')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai3')
# gm_mfc_3_flow = EpicsSignal('depo2w:USB231:3:Ai4', \
#     'write_pv' = depo2w:USB231:3:Ao1, \
# )
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai7')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ai8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:3:Ao2')
# gm_relay_4m = EpicsSignal('depo2w:USB231:3:Bo1')
# gm_relay_4a = EpicsSignal('depo2w:USB231:3:Bo2')
# gm_relay_3m = EpicsSignal('depo2w:USB231:3:Bo3')
# gm_relay_3a = EpicsSignal('depo2w:USB231:3:Bo4')
# gm_relay_2m = EpicsSignal('depo2w:USB231:3:Bo5')
# gm_relay_2a = EpicsSignal('depo2w:USB231:3:Bo6')
# gm_relay_1m = EpicsSignal('depo2w:USB231:3:Bo7')
# gm_relay_1a = EpicsSignal('depo2w:USB231:3:Bo8')
# gm_cm_1 = EpicsSignalRO('depo2w:USB231:4:Ai1')
# gm_cm_2 = EpicsSignalRO('depo2w:USB231:4:Ai2')
# im_cm_1 = EpicsSignalRO('depo2w:USB231:4:Ai3')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ai4')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ai5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ai6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ai7')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ai8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ao1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Ao2')
# gm_mfc_1_purge = EpicsSignal('depo2w:USB231:4:Bo1')
# gm_mfc_2_purge = EpicsSignal('depo2w:USB231:4:Bo2')
# gm_mfc_3_purge = EpicsSignal('depo2w:USB231:4:Bo3')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Bo4')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Bo5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Bo6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Bo7')
# #somealias = UnknownEpicsSignal('depo2w:USB231:4:Bo8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai2')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai3')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai4')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai7')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ai8')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ao1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Ao2')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo1')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo2')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo3')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo4')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo5')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo6')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo7')
# #somealias = UnknownEpicsSignal('depo2w:USB231:5:Bo8')
# gm_total_gas = EpicsSignalRO('depo2:userCalcOut41.A')
# gm_N2_percent = EpicsSignal('depo2:userCalcOut43.B')
# gm_O2_percent = EpicsSignal('depo2:userCalcOut44.B')
# pid2_setpoint = EpicsSignal('depo2:async_pid_slow2.VAL')
# pid2_p = EpicsSignal('depo2:async_pid_slow2.KP')
# pid2_i = EpicsSignal('depo2:async_pid_slow2.KI')
# pid2_d = EpicsSignal('depo2:async_pid_slow2.KD')
# pid2_fbon = EpicsSignal('depo2:async_pid_slow2.FBON')
# pid2_error = EpicsSignalRO('depo2:async_pid_slow2.ERR')
# pid2_readback = EpicsSignalRO('depo2:async_pid_slow2.CVAL')
# pid2_p_readback = EpicsSignalRO('depo2:async_pid_slow2.P', \
#     'write_pv' = depo2:async_pid_slow2.KP, \
# )
# pid2_i_readback = EpicsSignalRO('depo2:async_pid_slow2.I', \
#     'write_pv' = depo2:async_pid_slow2.KI, \
# )
# pid2_d_readback = EpicsSignalRO('depo2:async_pid_slow2.D', \
#     'write_pv' = depo2:async_pid_slow2.KD, \
# )
# pid3_setpoint = EpicsSignal('depo2:async_pid_slow3.VAL')
# pid3_p = EpicsSignal('depo2:async_pid_slow3.KP')
# pid3_i = EpicsSignal('depo2:async_pid_slow3.KI')
# pid3_d = EpicsSignal('depo2:async_pid_slow3.KD')
# pid3_fbon = EpicsSignal('depo2:async_pid_slow3.FBON')
# pid3_error = EpicsSignalRO('depo2:async_pid_slow3.ERR')
# pid3_readback = EpicsSignalRO('depo2:async_pid_slow3.CVAL')
# pid3_p_readback = EpicsSignalRO('depo2:async_pid_slow3.P', \
#     'write_pv' = depo2:async_pid_slow3.KP, \
# )
# pid3_i_readback = EpicsSignalRO('depo2:async_pid_slow3.I', \
#     'write_pv' = depo2:async_pid_slow3.KI, \
# )
# pid3_d_readback = EpicsSignalRO('depo2:async_pid_slow3.D', \
#     'write_pv' = depo2:async_pid_slow3.KD, \
# )
# GM_CM_1_ave = EpicsSignalRO('depo2:userAve10.VAL')
# GM_CM_1_samples = EpicsSignal('depo2:userAve10.A')
# GM_CM_1_precision = EpicsSignal('depo2:userAve10.PREC')
# GM_CM_2_ave = EpicsSignalRO('depo2:userAve11.VAL')
# GM_CM_2_samples = EpicsSignal('depo2:userAve11.A')
# GM_CM_2_precision = EpicsSignal('depo2:userAve11.PREC')
