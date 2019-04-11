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

# These load methods need some more work.  In the long run, would loke to be 
# able tp define the patterns in a script or in something like a json or yaml
# file initially but configurations which are read this way would be stored in
# a database with some reference ID, so that it can be referred to later.
def load_pattern_from_db(pattern_name):
    '''
    Assuming we get patterns into a db, with some ID as a key, pull the pattern
    associated with ID=pattern_name
    '''
    pass
    
def load_pattern_from_file(pattern_name):
    '''
    Load pattern from a file.  Should use some common format, json, yaml, ...
    Final format has not been defined.
    
    '''
    pass

def load_pattern_default():
    '''
    Initially we are using a defined pattern, stored in a dictionry.  This 
    provides some simplicity now.  Don't be rigid enough that this causes 
    problems later  
    '''
    return test_layers

def multi_layer(pattern_name = 'name', from_file=False, pattern_repeat = 1):
    
    """
    Set up to deposit multiple instances of a layering sequence
     This is the main script at this point.  To launch this, yow would type:
     RE(multi_layer(XXX))
     proper parameters should replace XXX 
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
        '''
            Take steps to coat a layer.  Separated into pre, do and post
            methods
        '''
        yield from pre_layer(layer)
        yield from do_mono_layer(layer)
        yield from post_layer(layer)
        
    def process_all_layers():
        '''
            Take care of the main coordinating the main steps of layers.
        overall creates n iterations of the loaded layer pattern.  The pattern 
        has multiple layers of multiple materials.  For each materal, controlled
        by changing guns, speed, number of layers, etc is settable.
        '''
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
    # Overall execution starts here,  reference back to the other inner methods
    pattern = get_pattern(pattern_name)        
    yield from process_all_layers()
    
#     @bpp.inject_md_decorator(md=_md)
#     def write_meta_data():
#         yield from _relay_setter("Disable", "Disable", "Disable")
#         
#     return (yield from write_meta_data())

def pre_layer( layer):
    ''' 
    Setup work to be done before doing the actual coating(mobe to starting
    position, prep the gun, ...
    '''
    def _prepare_layer():
        # bps.mv is basically a set.  pvs are treated like motors since that
        # was the first thing scanned
        yield from bps.mv(depos_sys.m1.velocity, layer['speed'])
        yield from bps.mv(depos_sys.m1, layer['start_position'])
        yield from bps.mv(depos_sys.gun_selector, layer['selected_gun'])
        print("%s start_position %s" % \
              (depos_sys.m1.name, depos_sys.m1.get()))
        print("%s velocity %s" % \
              (depos_sys.m1.name, depos_sys.m1.velocity.get()))
    
        return bps.sleep(layer['between_layer_time'])
    # Should try removing the return and just yield.  
    return (yield from _prepare_layer())
    
def do_mono_layer(layer):
    '''
    Actual coating done here.  When you get here you should be ready to go.
    Settings come from the pattern definition.
       - Enable the gun
       - loop for number of passes for the monolayer
          * start moving to end position
          * sleep between layers
          * Move back to the start position
    Some things will change here as we use the info in the gun to do the move
    '''
    logging.info("Starting Mono Layer %s" % layer['description'])
    yield from bps.mv(depos_sys.gun_selector.mps1_enable_output, 1)
    for l in range(layer['number_of_passes']):
        yield from bps.mv(layer['motor'], layer['end_position'])
        yield from bps.sleep(1)
        yield from bps.mv(layer['motor'], layer['start_position'])
        
def post_layer(layer):
    '''
    When  a layer is done clean up.  For now disable the gun (i.e. set the 
    gun selector to zero.  If this does not get more complex. can get rid of 
    do_post_layer, or pop it up an get rid of post_layer.
    '''
    def do_post_layer():
        yield from bps.mv(depos_sys.gun_selector, \
                          depos_sys.gun_selector.GUN_DISABLE_VAL)
    
    return (yield from do_post_layer())