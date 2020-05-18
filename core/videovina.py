import random
import os

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_slides':
        generate_slides(thisNode, app)

    elif knob_name == 'save_production':
        save_production_projects(thisNode)
    elif knob_name == 'refresh':
        refresh(thisNode)
    elif knob_name == 'generate_inputs':
        extra_picture_inputs(thisNode, app)


def refresh(thisNode):

    velocity = thisNode.velocity.get()
    rscale = thisNode.rscale.get()
    color = thisNode.color.get()
    speeds = thisNode.speeds.get()

    normal_speed = speeds[1]

    slide_frames = speeds[ velocity ]

    # esta velocidad de frames corresponde a la velocidad normal,
    # y calculta la velocidad final dependiendo de la velocidad de la slide
    transition_frames = thisNode.transition_duration.get()
    transition_frames = ( slide_frames * transition_frames ) / normal_speed
    # -------------------------

    print transition_frames


    first_frame = 1
    last_frame = slide_frames

    for i in range(1, 3):
        slide = thisNode.getNode('slide_' + str(i))
        frame_range = slide.getParam('FrameRangeframeRange')
        color_slide = slide.getParam('color')
        rscale_slide = slide.getParam('rscale')


        color_slide.set(color[0], color[1], color[2], color[3])
        rscale_slide.set(rscale)


        frame_range.set(first_frame, last_frame)





        # Transition
        transition = thisNode.getNode('transition_' + str(i))
        start_frame = last_frame - ( transition_frames / 2 )
        transition.getParam('start_frame').set( start_frame )
        transition.getParam('duration').set( transition_frames )
        # --------------------


        first_frame += slide_frames
        last_frame += slide_frames




def extra_picture_inputs(thisNode, app):

    amount = thisNode.input_amount.getValue()

    posx = 0
    for i in range(amount):
        _input = app.createNode('fr.inria.built-in.Input', 2, thisNode)
        _input.setPosition(posx, 0)

        posx += 200



def generate_slides(thisNode, app):

    count = thisNode.amount_slide.get()

    filter_dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
    filter_dot.setPosition(-300, 100)

    post_fx = app.createNode('fr.inria.built-in.BackDrop', 2, thisNode)
    post_fx.setScriptName('PostFX')
    post_fx.setLabel('Aqui van todos los efectos para el video completo.')
    post_fx.setColor(.5, .4, .4)
    post_fx.setSize(400, 500)
    post_fx_dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
    

    references_dir = thisNode.reference_pictures.get()
    references_pictures = os.listdir( references_dir )
    references_count = len( references_pictures )


    width = 1920
    hight = 1080

    posx = 0
    last_transition = None
    last_dot = None
    for i in range(count):


        slide = app.createNode('vv.slide', 2, thisNode)
        slide.setPosition(posx, 0)


        picture = references_dir + '/' + references_pictures[ random.randint(0, count) ]
        reader = app.createReader( picture, thisNode )
        reader.setPosition(posx - 12 , -350)
        
        reformat = app.createNode('net.sf.openfx.Reformat', 2, thisNode)
        reformat.getParam('reformatType').set(1)
        reformat.getParam('boxFixed').set(True)
        reformat.getParam('resize').set(4)
        reformat.getParam('boxSize').set(width, hight)
        reformat.setPosition(posx, -200)
        reformat.connectInput(0, reader)
        reformat.setColor(.5, .4, .4)

        slide.connectInput(0, reformat)


        if last_transition:
            last_transition.connectInput(1, slide)


        # si es el ultimo, conecta al output y cierra el loop
        if i == ( count - 1 ):

            post_fx.setPosition(posx - 50, 300)
            post_fx_dot.setPosition(posx + 45, 450)

            post_fx_dot.connectInput(0, last_transition)
            

            break

        # -----------------


        posx += 200


        transition = app.createNode('vv.FlareTransition', 2, thisNode)
        transition.setColor(.4, .5, .4)
        transition.setPosition(posx, 200)


        dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
        dot.setPosition(posx - 50, 100)

        
        


        

        
        

        transition.connectInput(2, dot)

        if last_dot:
            dot.connectInput(0, last_dot)
        else:
            dot.connectInput(0, filter_dot)



        if last_transition:
            transition.connectInput(0, last_transition)
        else:
            transition.connectInput(0, slide)

        last_transition = transition
        last_dot = dot
        


def save_production_projects(thisNode):
    print 'save_production'