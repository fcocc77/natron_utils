from natron_extent import getNode, createNode, alert, copy, warning, question
from slides import get_slides, get_slide, delete_slide
from vv_misc import get_resolution, connect_slide_inputs
from transition import directional_transition
import os
import random

# separacion de los nodos en horizontal
xdistance = 200
# ----------------


def refresh(thisNode, app, workarea):

    speed = thisNode.speed.get()
    _format = thisNode.format.get()
    color = thisNode.color.get()
    durations = thisNode.durations.get()

    normal_speed = durations[1]

    slide_frames = durations[speed]

    # esta velocidad de frames corresponde a la velocidad normal,
    # y calculta la velocidad final dependiendo de la velocidad de la slide
    transition_frames = thisNode.transition_duration.get()
    transition_frames = (slide_frames * transition_frames) / normal_speed
    # -------------------------

    width, hight = get_resolution(thisNode)

    slides = get_slides(workarea)

    # cambia la resolucion al primer y ultimo fondo negro
    first_black = getNode(workarea, 'FirstBlack')
    if not first_black:
        return
    first_black.getParam('size').set(width, hight)

    last_black = getNode(workarea, 'LastBlack')
    last_black.getParam('size').set(width, hight)
    # ---------------------

    mid_transition_frames = transition_frames / 2
    _last_frame = len(slides) * slide_frames
    # dissolve a negro en la ultima slide
    dissolve = getNode(workarea, 'last_transition').getParam('which')

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
    app.frameRange.set(1, _last_frame + transition_frames + 2)
    # --------------------

    first_frame = 1
    last_frame = slide_frames + mid_transition_frames

    for i, obj in enumerate(slides):
        slide = obj['slide']
        start_frame_slide = slide.getParam('start_frame')
        color_slide = slide.getParam('color')
        format_slide = slide.getParam('format')
        durations_slide = slide.getParam('durations')
        speed_slide = slide.getParam('speed')

        color_slide.set(color[0], color[1], color[2], color[3])
        speed_slide.set(speed)
        format_slide.set(_format)

        slide.getParam('prefix').set('slide_' + str(i))
        slide.getParam('refresh').trigger()

        if i == 0:
            # si es el primer frame, le suma la mitad de transicion a cada dimension
            durations_slide.set(
                durations[0] + mid_transition_frames,
                durations[1] + mid_transition_frames,
                durations[2] + mid_transition_frames)
        else:
            durations_slide.set(durations[0], durations[1], durations[2])

        start_frame_slide.set(first_frame)

        reformat = obj['reformat']
        if reformat:
            reformat.getParam('boxSize').set(width, hight)
            reformat.getParam('refresh').trigger()

        # Transition
        transition = obj['transition']
        if i == 0:
            # si es la primera transicion deja la transicion en el frame 1
            start_frame = 1
        else:
            start_frame = (last_frame - (transition_frames / 2)) - slide_frames

        transition_prefix = transition.getParam('prefix')
        if transition_prefix:
            transition_prefix.set('transition_' + str(i))
        transition.getParam('start_frame').set(start_frame)
        transition.getParam('duration').set(transition_frames)
        transition.getParam('format').set(_format)
        transition.getParam('speed').set(speed)
        transition.getParam('durations').set(durations[0], durations[1], durations[2])
        transition.getParam('color').set(color[0], color[1], color[2], color[3])
        transition.getParam('refresh').trigger()
        # --------------------

        # si es el primer slide, le sumamos la mitad de la duracion de la transicion,
        # ya que la primera transicion va a negro.
        if i == 0:
            first_frame += slide_frames + mid_transition_frames
        else:
            first_frame += slide_frames
        last_frame += slide_frames

        connect_slide_inputs(slides, i)


def generate_base_slides(thisNode, app, workarea):
    count = thisNode.amount_slide.get()

    filter_dot = getNode(workarea, 'filter_dot')
    if not filter_dot:
        filter_dot = app.createNode('fr.inria.built-in.Dot', 2, workarea)
        filter_dot.setLabel('filter_dot')
        filter_dot.setPosition(-300, 100)

    # slides existentes
    slides = get_slides(workarea)
    slides_count = len(slides)
    # --------------------

    # si la cantidad de slides a generar es menor de las que hay en el nodegraph
    # envia un mensage que se eliminaran algunas slides, si la respuesta es negativa retorna.
    count_delete_slide = None
    if count < slides_count:
        count_delete_slide = slides_count - count
        message = 'Actualmente tienes ' + \
            str(slides_count) + ' Slides y se eliminaran ' + \
            str(count_delete_slide) + ' Slides.'
        ok = question('Estas seguro de que quieres continuar ?', message)
        if not ok:
            return
    # --------------------------

    current_slides = 0

    if count_delete_slide:
        # borra las slides que sobran
        _range = range(slides_count - count_delete_slide, slides_count)
        delete_slide(workarea, _range)
        # -----------------------

        current_slides = slides_count - count_delete_slide
    else:
        width, hight = get_resolution(thisNode)
        posx = 0 - xdistance
        last_transition = getNode(
            workarea, 'slide_' + str(slides_count - 1) + '_transition')
        last_dot = getNode(workarea, 'slide_' + str(slides_count - 1) + '_dot')

        for i in range(count):
            posx += xdistance

            # si la slide ya fue generada, omite la creacion de la slide y pasa a la siguiente
            if slides_count - 1 >= i:
                continue
            # -------------------
            current_slides += 1

            slide_param = thisNode.getParam('slide')
            slide_id = 'vv.' + slide_param.getOption(slide_param.get())
            slide = app.createNode(slide_id, 2, workarea)
            slide_name = 'slide_' + str(i)
            slide.setLabel(slide_name)
            slide.setPosition(posx, 0)

            reformat = app.createNode('vv.ResolutionExpand', 2, workarea)
            reformat_name = 'slide_' + str(i) + '_reformat'
            reformat.setLabel(reformat_name)
            reformat.getParam('boxSize').set(width, hight)
            reformat.setPosition(posx, -200)
            reformat.setColor(.5, .4, .4)

            slide.connectInput(0, reformat)

            transition_param = thisNode.getParam('transition')
            transition_id = 'vv.' + transition_param.getOption(transition_param.get())
            transition = app.createNode(transition_id, 2, workarea)
            transition_name = 'slide_' + str(i) + '_transition'
            transition.setLabel(transition_name)
            transition.setColor(.4, .5, .4)
            transition.setPosition(posx, 200)
            transition.connectInput(1, slide)

            dot = app.createNode('fr.inria.built-in.Dot', 2, workarea)
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

    generate_random_pictures(thisNode, app, workarea,
                             current_slides + slides_count)
    update_post_fx(thisNode, workarea)
    refresh(thisNode, app, workarea)

    if current_slides:
        alert('Se han creado ' + str(current_slides) +
              ' Slides base.', 'VideoVina')


def update_post_fx(thisNode, workarea):
    slides = get_slides(workarea)
    if not len(slides):
        return

    # obtiene el primer y el ultimo nodo de transition
    first_transition = slides[0]['transition']
    last_transition = slides[-1]['transition']
    # -----------------------

    # Primer negro
    width, hight = get_resolution(thisNode)
    first_constant = getNode(workarea, 'FirstBlack')
    first_posx = first_transition.getPosition()[0]
    if not first_constant:
        first_constant = createNode(
            node='constant',
            label='FirstBlack',
            position=[first_posx - 200, 200],
            color=[.5, .5, .5],
            output=[0, first_transition],
            group=workarea
        )
        first_constant.getParam('extent').set(1)
        first_constant.getParam('reformat').set(True)
        first_constant.getParam('size').set(width, hight)
        first_constant.getParam('color').set(0, 0, 0, 1)
    # ---------------------

    # Ultimo negro
    last_constant = getNode(workarea, 'LastBlack')
    last_posx = last_transition.getPosition()[0]
    if not last_constant:
        last_constant = createNode(
            node='constant',
            label='LastBlack',
            color=[.5, .5, .5],
            group=workarea
        )
        last_constant.getParam('extent').set(1)
        last_constant.getParam('reformat').set(True)
        last_constant.getParam('size').set(width, hight)
        last_constant.getParam('color').set(0, 0, 0, 1)
    last_constant.setPosition(last_posx + 200, 100)
    # ---------------------

    # la ultima transition es un dissolve
    dissolve = getNode(workarea, 'last_transition')
    if not dissolve:
        dissolve = createNode(
            'dissolve',
            'last_transition',
            workarea,
            color=[.4, .5, .4]
        )
    dissolve.setPosition(last_posx + 200, 200)
    dissolve.disconnectInput(0)
    dissolve.connectInput(0, last_transition)
    dissolve.connectInput(1, last_constant)
    # -------------------------

    post_fx = getNode(workarea, 'PostFX')
    post_fx_dot = getNode(workarea, 'post_fx_dot')

    if not post_fx:
        post_fx = createNode(
            node='backdrop',
            label='PostFX',
            color=[.5, .4, .4],
            group=workarea
        )
        post_fx.getParam('Label').set(
            'Aqui van todos los efectos para el video completo.')
        post_fx.setSize(400, 500)
        post_fx_dot = createNode('dot', 'post_fx_dot', workarea)

    post_fx.setPosition(last_posx + 50, 300)
    post_fx_dot.setPosition(last_posx + 243, 900)
    post_fx_dot.disconnectInput(0)
    post_fx_dot.connectInput(0, dissolve)

    # VideoVina nodo como ultimo
    thisNode.setPosition(last_posx + 200, 1100)
    thisNode.connectInput(0, post_fx_dot)

    # nodo de vinarender
    vinarender = getNode(workarea, 'vinarender')
    if not vinarender:
        vinarender = createNode(
            node='vinarender',
            label='vinarender',
            group=workarea
        )
    vinarender.setPosition(last_posx + 200, 1200)
    vinarender.connectInput(0, thisNode)
    vinarender.setLabel('vinarender')
    vinarender.getParam('rgbonly').set(True)
    vinarender.getParam('project_frame_range').trigger()

    # si es que existe un viewer lo posiciona correctamente
    viewer = None
    for i in range(10):
        viewer = workarea.getNode('Viewer' + str(i))
        if viewer:
            viewer.setPosition(last_posx + 450, 895)
            viewer.disconnectInput(0)
            viewer.connectInput(0, post_fx_dot)
            break
    # ---------------------


def generate_random_pictures(thisNode, app, workarea, amount):

    references_dir = thisNode.reference_pictures.get()
    references_pictures = os.listdir(references_dir)
    references_count = len(references_pictures)

    index = random.randint(0, references_count - 1)

    random_pictures = []
    for i in range(amount):
        picture = references_dir + '/' + references_pictures[index]
        random_pictures.append(picture)

        index += 1
        if index >= references_count:
            index = 0

    generate_pictures(workarea, app, random_pictures)


def generate_pictures(workarea, app, pictures):
    for i, obj in enumerate(get_slides(workarea)):
        slide = obj['slide']
        reformat = obj['reformat']
        reader = obj['image']
        production = obj['production']

        # cuando se crea los slides en produccion, no se genera
        # el reformat, y se usa el slide para conectar
        if reformat:
            node_to_connect = reformat
        else:
            node_to_connect = slide
        # --------------------

        posx = node_to_connect.getPosition()[0] - 11
        posy = node_to_connect.getPosition()[1] - 200

        picture = pictures[i]

        # si la imagen ya fue generada, solo cambia el la imagen 'filename'
        if reader:
            reader.getParam('filename').set(picture)
        else:
            reader = app.createReader(picture, workarea)
            if production:
                reader_name = 'slide_' + str(i) + 'p_image'
            else:
                reader_name = 'slide_' + str(i) + '_image'
            reader.setLabel(reader_name)
            # deja la imagen con rgba para que no de conflicto, porque
            # a veces da conflicto al mezclar imagenes usando el shufle.
            reader.getParam('outputComponents').set(0)
            # ---------------------
            node_to_connect.connectInput(0, reader)
            if reformat:
                reformat.getParam('refresh').trigger()
        # -------------------------------
        reader.setPosition(posx, posy)
