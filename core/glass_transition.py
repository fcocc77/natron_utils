import random
from transition import directional_transition

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()


    if knob_name == 'seed':
        to_random(thisNode)

def to_random(thisNode):

    w = 1920

    seed = thisNode.seed.get()


    for i in range(1,8):
        
        width = thisNode.getNode('shape_width_' + str(i)).getParam('translate')
        position = thisNode.getNode('shape_position_' + str(i)).getParam('translate')



        random.seed(seed + 100 * i)
        random_width = random.randint(0, w / 5) 
        width.setValue(-random_width, 0)



        random.seed(seed + 1000 * i)
        random_position = random.randint(0, w) 
        # position.setValue(-random_position, 0)

        
        position_dst = -random_position
        position_src = position_dst - w


        directional_transition(position, 40, 0.8, 0.7, 10, [position_src, position_dst])
