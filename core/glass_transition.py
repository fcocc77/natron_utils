import random
from transition import directional_transition

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()
            
    if knob_name == 'refresh':

        sort = thisNode.sort.get()
        if sort == 0:
            to_random(thisNode)
        elif sort == 1:
            distribute(thisNode)

def distribute(thisNode):
    
    # parametros del grupo
    repetitions = thisNode.repetitions.get()
    gap = thisNode.gap.get()
    start_frame = thisNode.start_frame.get()
    duration = thisNode.duration.get()
    initial_translate = thisNode.initial_translate.get()
    end_translate = thisNode.end_translate.get()
    initial_rotate = thisNode.initial_rotate.get()
    initial_width = thisNode.initial_width.get()
    direction = thisNode.direction.get()
    # ------------------------

    # ajusta la direccion del la forma
    rotate = thisNode.getNode('direction_transform').getParam('rotate')
    if direction == 0:
        rotate.setValue(90)
    elif direction == 1:
        rotate.setValue(-90)
    elif direction == 2:
        rotate.setValue(0)
    elif direction == 3:
        rotate.setValue(180)    
    # ---------------------------

    w = 1920 + end_translate
    h = 1080

    exaggeration_time = 0.7
    exaggeration_value = 0.7

    part = w / repetitions
    left_translate = -end_translate

    rotate_src = initial_rotate
    rotate_dst = 0
    
    max_width = w / repetitions
    width_src = -initial_width 
    width_dst = -(part + 1)

    total_gap = 0

    for i in range(2, 8):
        thisNode.getNode('merge_' + str(i)).getParam('mix').set(0)

    for i in range(1, repetitions + 1):
        width = thisNode.getNode('shape_width_' + str(i)).getParam('translate')

        transform = thisNode.getNode('transform_' + str(i))
        rotate = transform.getParam('rotate')
        translate = transform.getParam('translate')
        center = transform.getParam('center')
        
        thisNode.getNode('merge_' + str(i)).getParam('mix').set(1)

        center.set( w - ( max_width / 2 ), h / 2)

        _start_frame = start_frame + total_gap

        directional_transition(rotate, duration, exaggeration_time, exaggeration_value, _start_frame, [rotate_src, rotate_dst])


        width.restoreDefaultValue(0)
        width.restoreDefaultValue(1)
        if direction == 3:
            directional_transition(width, duration, exaggeration_time, exaggeration_value, _start_frame, [width_src, - width_dst], dimension=1)
        else:
            directional_transition(width, duration, exaggeration_time, exaggeration_value, _start_frame, [width_src, width_dst])


        position_dst = -left_translate
        position_src = position_dst - initial_translate
        translate.restoreDefaultValue(0)
        translate.restoreDefaultValue(1)
        if direction == 3:
            directional_transition(translate, duration, exaggeration_time, 0.7, _start_frame, [position_src, position_dst], dimension=1)
        else:
            directional_transition(translate, duration, exaggeration_time, 0.7, _start_frame, [position_src, position_dst])

        total_gap += gap
        left_translate += part

def to_random(thisNode):

    w = 1920
    seed = thisNode.seed.get()

    for i in range(1,8):
        
        width = thisNode.getNode('shape_width_' + str(i)).getParam('translate')
        # position = thisNode.getNode('shape_position_' + str(i)).getParam('translate')

        random.seed(seed + 100 * i)
        random_width = random.randint(0, w / 5) 
        width.setValue(-random_width, 0)

        random.seed(seed + 1000 * i)
        random_position = random.randint(0, w) 

        position_dst = -random_position
        position_src = position_dst - w

        start_frame = random.randint(10, 20)

        # directional_transition(position, 70, 0.7, 0.7, start_frame, [position_src, position_dst])
