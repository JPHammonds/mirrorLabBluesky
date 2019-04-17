'''
This file sets up a set of PVs that will be logged in the mongo database.  
Note that the object name (e.g. depos_sys.gun_selector.mps1_power) is transformed
a bit when creating a name used to reference it.  To get a list of the names
used to reference these use:
db[-1].stream_names
To list the values stored for each of these use
db[-1].table(REF_NAME)    where REF_NAME is one of the names given by the stream_name
to plot these 
db[-1].table(REF_NAME).plot()

Note -1 in brackets on db tell it to retrieve the last record.  Can go back more
with -2, -3, ... or give a specific number for a particular run in the past.  Need 
to find a good way to get at a particular coating set.
'''
print(__file__)

sd = SupplementalData()
RE.preprocessors.append(sd)

sd.monitors.append(depos_sys.m1)
sd.monitors.append(depos_sys.m1.user_setpoint)
sd.monitors.append(depos_sys.m1.velocity)
sd.monitors.append(depos_sys.gun_selector.mps1_power)
sd.monitors.append(depos_sys.gun_selector.mps1_voltage)
sd.monitors.append(depos_sys.gun_selector.mps1_current)
sd.monitors.append(depos_sys.gun_selector.mps1_voltage_rbv)
sd.monitors.append(depos_sys.gun_selector.mps1_current_rbv)
sd.monitors.append(depos_sys.gun_selector.mps1_power_rbv)
sd.monitors.append(depos_sys.gun_selector.guns.gun1.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun2.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun3.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun4.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun5.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun6.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun7.voltage_avg)
sd.monitors.append(depos_sys.gun_selector.guns.gun8.voltage_avg)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc1.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc2.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc3.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc4.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc5.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc6.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc7.flow)
sd.monitors.append(depos_sys.gas_mixer.mfcs.mfc8.flow)

