import random
import os
import NatronGui
from natron_utils import copy, getNode, question, alert, createNode
from transition import directional_transition

# separacion de los nodos en horizontal
xdistance = 200
# ----------------

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_slides':
        generate_slides(thisNode, app)
        refresh(thisNode, app)
    elif knob_name == 'save_production':
        save_production_projects(thisNode)
    elif knob_name == 'refresh':
        refresh(thisNode, app)
    elif knob_name == 'generate_inputs':
        extra_picture_inputs(thisNode, app)
    elif knob_name == 'duplicate_slides':
        duplicate_slides(thisNode, app)
        refresh(thisNode, app)

def refresh(thisNode, app):

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
    
    width, hight = get_resolution(thisNode)
    
    slides = get_slides(thisNode)

    # cambia la resolucion al primer y ultimo fondo negro
    first_black = getNode(thisNode, 'FirstBlack')
    first_black.getParam('size').set(width, hight)

    last_black = getNode(thisNode, 'LastBlack')
    last_black.getParam('size').set(width, hight)
    # ---------------------


    mid_transition_frames = transition_frames / 2 
    _last_frame = len(slides) * slide_frames
    # dissolve a negro en la ultima slide
    dissolve = getNode(thisNode, 'last_transition').getParam('which')

    directional_transition(
        dissolve, 
        transition_frames, 
        0.5, 0.5, 
        _last_frame, 
        [0, 1]
    )
    # -------------------

    # cambia el rango de 'Project Settings', dependiendo de la cantidad de slides
    # le sumamos 'transition_frames' que equivale a 2 mitades de transicion, la inicial y la final
    app.frameRange.set(1, _last_frame + transition_frames + 2 )
    # --------------------

    first_frame = 1
    last_frame = slide_frames + mid_transition_frames

    for i, obj in enumerate(slides):
        slide = obj['slide']
        frame_range = slide.getParam('FrameRangeframeRange')
        color_slide = slide.getParam('color')
        rscale_slide = slide.getParam('rscale')

        color_slide.set(color[0], color[1], color[2], color[3])
        rscale_slide.set(rscale)

        frame_range.set(first_frame, last_frame)

        # Transition
        transition = obj['transition']
        if i == 0:
            # si es la primera transicion deja la transicion en el frame 1
            start_frame = 1
        else:
            start_frame = ( last_frame - ( transition_frames / 2 ) ) - slide_frames
        transition.getParam('start_frame').set( start_frame )
        transition.getParam('duration').set( transition_frames )
        transition.getParam('refresh').trigger()
        # --------------------

        reformat = obj['reformat']
        reformat.getParam('boxSize').set(width, hight)
        reformat.getParam('refresh').trigger()

        # si es el primer slide, le sumamos la mitad de la duracion de la transicion,
        # ya que la primera transicion va a negro.
        if i == 0:
            first_frame += slide_frames + mid_transition_frames
        else:
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

        if not reformat:
            continue

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
            reformat.getParam('refresh').trigger()
        # -------------------------------
        reader.setPosition(posx, posy)

        index += 1
        if index >= references_count:
            index = 0 

def delete_slide(thisNode, slide_number):
    # se usa .destroy() 2 veces ya que a veces
    # natron no borra el nodo
    def remove(index):
        obj = get_slide(thisNode, index)
        for key, node in obj.iteritems():
            if node:
                node.destroy()

    if type(slide_number) is list:
        for i in slide_number:
            remove(i)
        for i in slide_number:
            remove(i)
    else:
        remove(slide_number)
        remove(slide_number)

def get_resolution(thisNode):
    # obtiene la correcta resolucion a partir de una escala
    # tomando como referencia el 1920x1080
    rscale = thisNode.rscale.get()

    width = 1920 * rscale
    hight = 1080 * rscale

    return [width, hight]

def generate_black():
    None

def generate_slides(thisNode, app):
    count = thisNode.amount_slide.get()

    filter_dot = getNode(thisNode, 'filter_dot')
    if not filter_dot:
        filter_dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
        filter_dot.setLabel('filter_dot')
        filter_dot.setPosition(-300, 100)
    
    # slides existentes
    slides = get_slides(thisNode)
    slides_count = len(slides)
    # --------------------
    
    # si la cantidad de slides a generar es menor de las que hay en el nodegraph
    # envia un mensage que se eliminaran algunas slides, si la respuesta es negativa retorna.
    count_delete_slide = None
    if count < slides_count:
        count_delete_slide = slides_count - count
        message = 'Actualmente tienes ' + str(slides_count) + ' Slides y se eliminaran ' + str(count_delete_slide) + ' Slides.'
        ok = question('Estas seguro de que quieres continuar ?', message) 
        if not ok:
            return
    # --------------------------

    width, hight = get_resolution(thisNode)

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
        
        reformat = app.createNode('vv.ResolutionExpand', 2, thisNode)
        reformat_name = 'slide_' + str(i) + '_reformat'
        reformat.setLabel(reformat_name)
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
            None


        last_transition = transition
        last_dot = dot
    
    # borra las slides que sobran
    if count_delete_slide:
        _range = range(slides_count - count_delete_slide, slides_count)
        delete_slide(thisNode, _range)
    # -----------------------

    generate_pictures(thisNode, app)
    update_post_fx(thisNode, app)

    
    if created_slides:
        NatronGui.natron.informationDialog('VideoVina', 'Se han creado ' + str(created_slides) + ' Slides base.')
     
def get_slide(thisNode, index):
    _index = str(index)

    slide = getNode(thisNode, 'slide_' + _index)
    reformat = getNode(thisNode, 'slide_' + _index + '_reformat')
    image = getNode(thisNode, 'slide_' + _index + '_image')
    transition = getNode(thisNode, 'slide_' + _index + '_transition')
    dot = getNode(thisNode, 'slide_' + _index + '_dot')

    return {
        'slide' : slide,
        'reformat' : reformat,
        'image' : image,
        'transition' : transition,
        'dot' : dot
    }

def get_slides(thisNode):
    slides = []

    for i in range(100):        
        obj = get_slide(thisNode, i)
        if obj['slide']:
            slides.append(obj)

    return slides

def update_post_fx(thisNode, app):
    # obtiene el primer y el ultimo nodo de transition
    slides = get_slides(thisNode)
    first_transition = slides[0]['transition']
    last_transition = slides[-1]['transition']
    # -----------------------

    # Primer negro
    width, hight = get_resolution(thisNode)
    first_constant = getNode(thisNode, 'FirstBlack')
    first_posx = first_transition.getPosition()[0]
    if not first_constant:
        first_constant = createNode(
            node='constant', 
            label='FirstBlack', 
            position=[first_posx - 200, 200], 
            color=[.5, .5, .5],
            output=[ 0, first_transition ],
            group=thisNode
        )
        first_constant.getParam('extent').set(1)
        first_constant.getParam('reformat').set(True)
        first_constant.getParam('size').set(width, hight)
    # ---------------------

    # Ultimo negro
    last_constant = getNode(thisNode, 'LastBlack')
    last_posx = last_transition.getPosition()[0]
    if not last_constant:
        last_constant = createNode(
            node='constant', 
            label='LastBlack',
            color=[.5, .5, .5],
            group=thisNode
        )
        last_constant.getParam('extent').set(1)
        last_constant.getParam('reformat').set(True)
        last_constant.getParam('size').set(width, hight)
    last_constant.setPosition( last_posx + 200, 100 )
    # ---------------------

    # la ultima transition es un dissolve
    dissolve = getNode(thisNode, 'last_transition')
    if not dissolve:
        dissolve = createNode(
            'dissolve', 
            'last_transition', 
            thisNode
        )
    dissolve.setPosition( last_posx + 200, 200 )
    dissolve.disconnectInput(0)
    dissolve.connectInput(0, last_transition)
    dissolve.connectInput(1, last_constant)
    # -------------------------

    post_fx = getNode(thisNode, 'PostFX')
    post_fx_dot = getNode(thisNode, 'post_fx_dot')

    if not post_fx:
        post_fx = createNode(
            node = 'backdrop', 
            label = 'PostFX',
            color = [.5, .4, .4],
            group = thisNode
        )
        post_fx.getParam('Label').set('Aqui van todos los efectos para el video completo.')
        post_fx.setSize(400, 500)
        post_fx_dot = createNode('dot', 'post_fx_dot', thisNode)

    post_fx.setPosition(last_posx + 50, 300)
    post_fx_dot.setPosition(last_posx + 245, 450)
    post_fx_dot.disconnectInput(0)
    post_fx_dot.connectInput(0, dissolve)    

def duplicate_slides(thisNode, app):
    # duplica los slides base, dependiendo de la
    # cantidad de fotos que importemos.

    base_amount = thisNode.amount_slide.get()
    amount = thisNode.production_slides.get()

    slides = get_slides(thisNode)
    base_count = len( slides )

    if amount <= base_amount: 
        NatronGui.natron.warningDialog( 'Production Slides', 'La Cantidad de slides tiene que ser mayor que los slides base.' )
        return
    
    if amount <= base_count:
        NatronGui.natron.warningDialog( 'Production Slides', 'Ya existen los ' + str(amount) + ' Slides, Aumente la cantidad si quiere mas.' )
        return

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
        dot_name = 'slide_' + str(index) + '_dot'
        dot.setLabel(dot_name)
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

    update_post_fx(thisNode, app)
    generate_pictures(thisNode, app)

def save_production_projects(thisNode):
    print 'save_production'