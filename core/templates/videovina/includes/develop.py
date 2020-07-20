from nx import getNode, createNode, alert, copy, warning, question, app
from vina import get_videovina, get_ranges, videovina_data, get_transition_duration
from slides import get_slides, get_slide, delete_slide, get_first_slide
from vv_misc import get_resolution
from transition import directional_transition
from pictures import get_picture
import os
import random

# separacion de los nodos en horizontal
xdistance = 200
# ----------------


def refresh(thisNode, app, workarea):
    vina = videovina_data()

    speed = vina.speed
    _format = vina.format
    color = vina.color
    durations = vina.durations

    slide_duration = durations[speed]

    width, hight = get_resolution(thisNode)

    slides = get_slides(workarea)
    slide_count = slides[-1]['index'] + 1  # index del ultimo slide

    # cambia la resolucion al primer y ultimo fondo negro
    first_black = getNode(workarea, 'FirstBlack')
    if not first_black:
        return
    first_black.getParam('size').set(width, hight)

    last_black = getNode(workarea, 'LastBlack')
    last_black.getParam('size').set(width, hight)
    # ---------------------

    transition_frames = get_transition_duration()
    mid_transition_frames = transition_frames / 2
    _last_frame = slide_count * slide_duration
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
    app.getProjectParam('frameRange').set(1, _last_frame + transition_frames + 2)
    # --------------------

    frame_range_list = get_ranges(slide_count, speed)

    for obj in slides:
        slide = obj['slide']
        index = obj['index']
        start_frame_slide = slide.getParam('start_frame')
        color_slide = slide.getParam('color')
        format_slide = slide.getParam('format')
        durations_slide = slide.getParam('durations')
        speed_slide = slide.getParam('speed')

        color_slide.set(color[0], color[1], color[2], color[3])
        speed_slide.set(speed)
        format_slide.set(_format)

        slide.getParam('prefix').set('slide_' + str(index))
        slide.getParam('refresh').trigger()

        if index == 0:
            # si es el primer slide, le suma la mitad de transicion a cada dimension
            durations_slide.set(
                durations[0] + mid_transition_frames,
                durations[1] + mid_transition_frames,
                durations[2] + mid_transition_frames)
        else:
            durations_slide.set(durations[0], durations[1], durations[2])

        first_frame, last_frame = frame_range_list[index]

        start_frame_slide.set(first_frame)

        picture = get_picture(workarea, index)
        if picture:
            reformat = picture['reformat']
            reformat.getParam('boxSize').set(width, hight)
            reformat.getParam('refresh').trigger()

        # Transition
        transition = obj['transition']
        if index == 0:
            # si es la primera transicion deja la transicion en el frame 1
            start_frame = 1
        else:
            start_frame = (last_frame - (transition_frames / 2)) - slide_duration

        transition_prefix = transition.getParam('prefix')
        if transition_prefix:
            transition_prefix.set('transition_' + str(index))
        transition.getParam('start_frame').set(start_frame)
        transition.getParam('duration').set(transition_frames)
        transition.getParam('format').set(_format)
        transition.getParam('speed').set(speed)
        transition.getParam('durations').set(durations[0], durations[1], durations[2])
        transition.getParam('color').set(color[0], color[1], color[2], color[3])
        transition.getParam('refresh').trigger()
        # --------------------

        connect_slide_inputs(workarea, index, vina.pictures_amount)


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

    update_post_fx(thisNode, workarea)
    refresh(thisNode, app, workarea)

    if current_slides:
        alert('Se han creado ' + str(current_slides) +
              ' Slides base.', 'VideoVina')


def update_post_fx(thisNode=None, workarea=None):
    if not thisNode:
        thisNode = get_videovina()
    if not workarea:
        workarea = app()

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
    thisNode.disconnectInput(0)
    thisNode.connectInput(0, post_fx_dot)

    # nodo de vinarender
    vinarender = getNode(workarea, 'vinarender')
    if not vinarender:
        vinarender = createNode(
            node='vinarender',
            group=workarea
        )
        vinarender.setLabel('vinarender')
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

    # conecta el primer slide al primer dot y negro
    first_slide = get_first_slide(workarea)
    filter_dot = getNode(workarea, 'filter_dot')
    first_black = getNode(workarea, 'FirstBlack')
    first_slide['dot'].connectInput(0, filter_dot)
    first_slide['transition'].connectInput(0, first_black)


def connect_slide_inputs(workarea, current_slide, max_pictures):
    # conecta todas las entradas de cada slide, asi
    # poder usarlas dentro del grupo de la slide
    obj = get_slide(workarea, current_slide)
    if not obj:
        return
    slide = obj['slide']

    extra_count = slide.getMaxInputCount() - 1

    if not extra_count:
        return

    connect_nodes_count = max_pictures - 1

    def connect_input(_input, connect_node):
        slide.disconnectInput(_input)
        picture = get_picture(workarea, connect_node)
        reformat = picture['reformat']
        image = picture['image']
        if reformat:
            slide.connectInput(_input, reformat)
        else:
            slide.connectInput(_input, image)

    if connect_nodes_count >= extra_count:
        # encuentra el nodo de inicio, para las conecciones
        connect_node = current_slide - (extra_count / 2)

        # el index maximo al que se puede conectar una entrada
        max_connection = connect_node + extra_count
        # -------------------

        # si los nodos para poder conectarse, superan a las necesarias, encuentra
        # un nodo posible
        if max_connection >= connect_nodes_count:
            connect_node = connect_nodes_count - extra_count
        # -------------------

        if connect_node < 0:
            connect_node = 0

        # la entrada 0 pertenece a la imagen principal, por eso inicia del 1
        for i in range(1, extra_count + 1):
            if connect_node == current_slide:
                connect_node += 1

            connect_input(i, connect_node)
            connect_node += 1
    else:
        # va conectando a todas los nodos posible, cuando se
        # terminan vuelve a 0 y comienza a conectar otra vez
        connect_node = 0
        for i in range(1, extra_count + 1):
            if connect_node == current_slide:
                connect_node += 1

            if connect_node > connect_nodes_count:
                connect_node = 0

            # cuando es la primera slide se conecta a si mismo,
            # asi que cuando la acutal slide sea 0 y el nodo a conectar 0
            # cambia el nodo a conectar a 1.
            if current_slide == 0 and connect_node == 0:
                connect_node = 1
            # ------------------

            connect_input(i, connect_node)
            connect_node += 1
