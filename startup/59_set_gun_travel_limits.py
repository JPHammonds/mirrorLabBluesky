'''
This file sets gun parameters used in calculating positions that do not change
very often.  These should be parameters that only change when something chang
in instrumentation on the deposition system.
'''
depos_sys.gun_selector.guns.gun1.set_travel_limits(mask_width=40, zero_position=1111.2, overspray=45)
depos_sys.gun_selector.guns.gun2.set_travel_limits(mask_width=40, zero_position=1318.4, overspray=45)
depos_sys.gun_selector.guns.gun3.set_travel_limits(mask_width=40, zero_position=1517.6, overspray=45)
depos_sys.gun_selector.guns.gun4.set_travel_limits(mask_width=40, zero_position=1720.8, overspray=45)
depos_sys.gun_selector.guns.gun5.set_travel_limits(mask_width=142, zero_position=2962.225, overspray=45)
depos_sys.gun_selector.guns.gun6.set_travel_limits(mask_width=142, zero_position=3247.98, overspray=45)
depos_sys.gun_selector.guns.gun7.set_travel_limits(mask_width=142, zero_position=3533.7, overspray=45)
depos_sys.gun_selector.guns.gun8.set_travel_limits(mask_width=40, zero_position=4594.2, overspray=45)
