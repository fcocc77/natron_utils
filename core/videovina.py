import random
import os
import NatronGui
from natron_utils import copy, getNode, question

# separacion de los nodos en horizontal
xdistance = 200
# ----------------

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
    elif knob_name == 'duplicate_slides':
        duplicate_slides(thisNode, app)

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

    first_frame = 1
    last_frame = slide_frames

    slides = get_slides(thisNode)

    for obj in slides:
        slide = obj['slide']
        frame_range = slide.getParam('FrameRangeframeRange')
        color_slide = slide.getParam('color')
        rscale_slide = slide.getParam('rscale')

        color_slide.set(color[0], color[1], color[2], color[3])
        rscale_slide.set(rscale)

        frame_range.set(first_frame, last_frame)

        # Transition
        transition = obj['transition']
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

def generate_pictures(thisNode, app):

    references_dir = thisNode.reference_pictures.get()
    references_pictures = os.listdir( references_dir )
    references_count = len( references_pictures )

    index = random.randint(0, references_count - 1)

    for i, obj in enumerate( get_slides(thisNode) ):
        reformat = obj['reformat']
        reader = obj['image']

        posx = reformat.getPosition()[0] - 11
        posy = reformat.getPosition()[1] - 200

        picture = references_dir + '/' + references_pictures[index]
        
        # si la imagen ya fue generada, solo cambia el la imagen 'filename'
        if reader:
            reader.getParam('filename').set(picture)
        else:
            reader = app.createReader( picture, thisNode )
            reader_name = 'slide_' + str(i) + '_image'
            reader.setLabel(reader_name)
            reformat.connectInput(0, reader)
        # -------------------------------
        reader.setPosition(posx, posy)

        index += 1
        if index >= references_count:
            index = 0 

def generate_slides(thisNode, app):
    count = thisNode.amount_slide.get()

    filter_dot = getNode(thisNode, 'filter_dot')
    if not filter_dot:
        filter_dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
        filter_dot.setLabel('filter_dot')
        filter_dot.setPosition(-300, 100)
    
    post_fx = getNode(thisNode, 'PostFX')
    post_fx_dot = getNode(thisNode, 'post_fx_dot')
    if not post_fx:
        post_fx = app.createNode('fr.inria.built-in.BackDrop', 2, thisNode)
        post_fx.setLabel('PostFX')
        post_fx.getParam('Label').set('Aqui van todos los efectos para el video completo.')
        post_fx.setColor(.5, .4, .4)
        post_fx.setSize(400, 500)
        post_fx_dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
        post_fx_dot.setLabel('post_fx_dot')


    # slides existentes
    slides = get_slides(thisNode)
    slides_count = len(slides)
    # --------------------
    
    # si la cantidad de slides a generar es menor de las que hay en el nodegraph
    # envia un mensage que se eliminaran algunas slides, si la respuesta es negativa retorna.
    if count < slides_count:
        message = 'Actualmente tienes ' + str(slides_count) + ' Slides y se eliminaran ' + str(slides_count - count) + ' Slides.'
        ok = question('Estas seguro de que quieres continuar ?', message) 
        if not ok:
            return
    # --------------------------

    width = 1920
    hight = 1080

    posx = 0 - xdistance
    last_transition = getNode(thisNode, 'slide_' + str( slides_count - 1 ) + '_transition')
    last_dot = getNode(thisNode, 'slide_' + str( slides_count - 1 ) + '_dot')
    
    created_slides = 0
    for i in range(count):
        posx += xdistance

        # si la slide ya fue generada, omite la creacion de la slide y pasa a la siguiente
        if slides_count - 1 >= i:
            continue
        # -------------------
        created_slides += 1

        slide = app.createNode('vv.slide', 2, thisNode)
        slide_name = 'slide_' + str(i)
        slide.setLabel(slide_name)
        slide.setPosition(posx, 0)
        
        reformat = app.createNode('net.sf.openfx.Reformat', 2, thisNode)
        reformat_name = 'slide_' + str(i) + '_reformat'
        reformat.setLabel(reformat_name)
        reformat.getParam('reformatType').set(1)
        reformat.getParam('boxFixed').set(True)
        reformat.getParam('resize').set(4)
        reformat.getParam('boxSize').set(width, hight)
        reformat.setPosition(posx, -200)
        reformat.setColor(.5, .4, .4)

        slide.connectInput(0, reformat)

        transition = app.createNode('vv.FlareTransition', 2, thisNode)
        transition_name = 'slide_' + str(i) + '_transition'
        transition.setLabel(transition_name)
        transition.setColor(.4, .5, .4)
        transition.setPosition(posx, 200)
        transition.connectInput(1, slide)

        dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
        dot_name = 'slide_' + str(i) + '_dot'
        dot.setLabel(dot_name)
        dot.setPosition(posx - 50, 100)
    
        transition.connectInput(2, dot)

        if last_dot:
            dot.connectInput(0, last_dot)
        else:
            dot.connectInput(0, filter_dot)

        if last_transition:
            transition.connectInput(0, last_transition)
        else:
            constant = app.createNode('net.sf.openfx.ConstantPlugin', 2, thisNode)
            constant.setLabel('FirstBlack')
            constant.setColor(.5, .5, .5)
            constant.setPosition(posx - 200, 200)
            transition.connectInput(0, constant)

        last_transition = transition
        last_dot = dot

        # si es el ultimo, conecta al output y cierra el loop
        if i == count - 1:
            post_fx.setPosition(posx - 150, 300)
            post_fx_dot.setPosition(posx + 45, 450)
            post_fx_dot.disconnectInput(0)
            post_fx_dot.connectInput(0, last_transition)
        # -----------------

    generate_pictures(thisNode, app)
    
    if created_slides:
        NatronGui.natron.informationDialog('VideoVina', 'Se han creado ' + str(created_slides) + ' Slides base.')
     
def get_slides(thisNode):

    slides = []

    for i in range(100):
        slide = getNode(thisNode, 'slide_' + str(i))
        reformat = getNode(thisNode, 'slide_' + str(i) + '_reformat')
        image = getNode(thisNode, 'slide_' + str(i) + '_image')
        transition = getNode(thisNode, 'slide_' + str(i) + '_transition')
        if slide:
            slides.append({
                'slide' : slide,
                'reformat' : reformat,
                'image' : image,
                'transition' : transition
            })

    return slides

def duplicate_slides(thisNode, app):
    # duplica los slides base, dependiendo de la
    # cantidad de fotos que importemos.

    amount = thisNode.production_slides.get()
    
    slides = get_slides(thisNode)
    base_count = len( slides )

    last_transition = None
    last_dot = None
 
    last_base_transition = getNode(thisNode, 'slide_' + str( base_count - 1 ) + '_transition')
    last_base_dot = getNode(thisNode, 'slide_' + str( base_count - 1 ) + '_dot')

    current = 0
    posx = ( xdistance * base_count ) + xdistance
    for i in range( amount - base_count ):
        index = i + base_count

        slide = slides[current]['slide']
        reformat = slides[current]['reformat']
        transition = slides[current]['transition']

        # new_image = copy(image, thisNode)
        # new_image.setPosition(posx, -400)
        
        new_reformat = copy(reformat, thisNode)
        new_reformat.setColor(.4, .5, .7)
        new_reformat.setPosition(posx, -200)
        new_reformat.setLabel('slide_' + str(index) + '_reformat')

        new_slide = copy(slide, thisNode)
        new_slide.setPosition(posx, 0)
        new_slide.setLabel('slide_' + str(index))
        new_slide.connectInput(0, new_reformat)

        new_transition = copy(transition, thisNode)
        new_transition.setColor(.7, .7, .4)
        new_transition.setPosition(posx, 200)
        new_transition.setLabel('slide_' + str(index) + '_transition')
        if last_transition:
            new_transition.connectInput(0, last_transition)
        else:
            new_transition.connectInput(0, last_base_transition)


        new_transition.connectInput(1, new_slide)

        dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
        dot.setPosition(posx - 50, 100)
    
        if last_dot:
            dot.connectInput(0, last_dot)
        else:
            dot.connectInput(0, last_base_dot)


        new_transition.connectInput(2, dot)


        last_transition = new_transition
        last_dot = dot

        current += 1
        if current >= base_count:
            current = 0
        
        posx += xdistance

    # mueve el backdrop 'postfx' hacia el ultimo nodo creado
    post_fx = getNode(thisNode, 'PostFX')
    post_fx.setPosition(posx - 350, 300)
    post_fx_dot = getNode(thisNode, 'post_fx_dot')
    post_fx_dot.disconnectInput(0)
    post_fx_dot.connectInput(0, last_transition)
    post_fx_dot.setPosition(posx - 157, 450)
    # ------------------

    generate_pictures(thisNode, app)

def save_production_projects(thisNode):
    print 'save_production'