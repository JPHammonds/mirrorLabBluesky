from imageio.plugins._tifffile import sequence
print(__file__)
import logging
import bluesky.plan_stubs as bps
from bluesky import preprocessors as bpp
import time
import databroker

test_layers = [
    {'speed': 36.5, 'motor': depos_sys.m1, 'start_position':1262,
     'end_position': 1402, 'selected_gun': 3,
     'between_layer_time': 5, 'number_of_passes':10, 'description': 'Cd'},
#     {'speed': 36.10691, 'motor': depos_sys.m1, 'start_position':3207,
#      'end_position': 3449, 'selected_gun': 7,
#      'between_layer_time':5, 'number_of_passes':1, 'description': 'B4C'}
    ]

def load_pattern_from_db(pattern_name):
    pass
    
def load_pattern_from_file(pattern_name):
    pass

def load_pattern_default():
    return test_layers

def multi_layer(pattern_name = 'name', from_file=False, pattern_repeat = 1):
    
    """pa
    Set up to deposit multiple instances of a layering sequence
    """
    def get_pattern(pattern_name):

        pattern = {}
        if pattern_name == "default":
            pattern = load_pattern_default()
        elif from_file:
            pattern = load_pattern_from_file(pattern_name)
        else:
            pattern = load_pattern_from_db(pattern_name)
        return pattern
    
    def process_multilayer(layer_num, layer):
        yield from pre_layer(layer)
        yield from do_mono_layer(layer)
        yield from post_layer(layer)
        
    def process_all_layers():
        for i in range(pattern_repeat):
#             _md['multi_layer'][str(i+1)] = {}
            sub_layer=1
            for layer in pattern:
                yield from bps.mv(depos_sys.m1.velocity, layer['speed'], \
                                  depos_sys.m1, )
                #yield from bps.trigger_and_read(depos_sys)
                yield from process_multilayer(i+1, layer)
                sub_layer += 1
#             _md['end_time'] = time.ctime()
    
    pattern = get_pattern(pattern_name)        
    yield from process_all_layers()
    
#     @bpp.inject_md_decorator(md=_md)
#     def write_meta_data():
#         yield from _relay_setter("Disable", "Disable", "Disable")
#         
#     return (yield from write_meta_data())

def pre_layer( layer):
#     pass
    def _prepare_layer():
        yield from bps.mv(depos_sys.m1.velocity, layer['speed'])
        yield from bps.mv(depos_sys.m1, layer['start_position'])
        yield from bps.mv(depos_sys.gun_selector, layer['selected_gun'])
        print("%s start_position %s" % \
              (depos_sys.m1.name, depos_sys.m1.get()))
        print("%s velocity %s" % \
              (depos_sys.m1.name, depos_sys.m1.velocity.get()))
    
        return bps.sleep(layer['between_layer_time'])
    return (yield from _prepare_layer())
    
def do_mono_layer(layer):
    logging.info("Starting Mono Layer %s" % layer['description'])
    yield from bps.mv(depos_sys.gun_selector.mps1_enable_output, 1)
    for l in range(layer['number_of_passes']):
        yield from bps.mv(layer['motor'], layer['end_position'])
        yield from bps.sleep(1)
        yield from bps.mv(layer['motor'], layer['start_position'])
        
def post_layer(layer):
    def do_post_layer():
        yield from bps.mv(depos_sys.gun_selector, \
                          depos_sys.gun_selector.GUN_DISABLE_VAL)
    
    return (yield from do_post_layer())