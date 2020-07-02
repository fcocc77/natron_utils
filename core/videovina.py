import random
import os
import shutil
from natron_utils import copy, getNode, question, alert, createNode, warning, get_parent
from transition import directional_transition
from util import jread, jwrite
from time import sleep
from general import formats

# separacion de los nodos en horizontal
xdistance = 200
# ----------------


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    workarea = get_parent(thisNode)

    knob_name = thisParam.getScriptName()

    project_path = os.path.dirname(os.path.dirname(app.projectPath.get()))

    if knob_name == 'generate_slides':
        generate_base_slides(thisNode, app, workarea)

    elif knob_name == 'save_production':
        save_production_projects(thisNode)

    elif knob_name == 'refresh':
        refresh(thisNode, app, workarea)

    elif knob_name == 'generate_inputs':
        extra_picture_inputs(thisNode, app, workarea)

    elif knob_name == 'duplicate_slides':
        duplicate_slides(thisNode, app, workarea)

    elif knob_name == 'videovina_info':
        export_videovina_info(thisNode, app, workarea, project_path)

    elif knob_name == 'update_videovina_project':
        update_videovina_project(thisNode, app, workarea)

    elif knob_name == 'export_default_project':
        export_default_project(thisNode, app, workarea, project_path)

    elif knob_name == 'default_color':
        set_default_color(thisNode, thisParam)

    elif knob_name == 'include_texts':
        color_if_has_text(thisNode, thisParam)

    elif knob_name == 'videovina_root':
        update_private_content(thisNode, thisParam)

    elif knob_name == 'play':
        play_song(thisNode)

    elif knob_name == 'stop':
        play_song(thisNode, play=False)

    elif knob_name == 'transfer_to_static':
        transfer_to_static(thisNode, app, project_path)


def play_song(thisNode, play=True):
    if not play:
        os.system('pkill -9 vlc')
        return

    cmd = 'vlc --qt-start-minimized "' + get_current_song(thisNode)[1] + '"'

    os.system('pkill -9 vlc')
    os.popen2(cmd)


def get_type_song(thisNode, song_name):
    for option in thisNode.getParam('default_song').getOptions():
        if song_name in option:
            song_type = option.split('-')[1].strip().lower()
            return song_type


def get_current_song(thisNode):
    default_song = thisNode.getParam('default_song')
    private = thisNode.getParam('videovina_root').get() + '/private'

    song = default_song.getOption(default_song.get())
    song_type = song.split('-')[1].strip().lower()
    song_name = song.split('-')[0].strip()
    song_path = private + '/music/' + song_type + '/' + song_name + '.mp3'

    return [song_name, song_path, song_type]


def update_private_content(thisNode, thisParam):
    # actualiza todo el contenido que hay en la carpeta private de videovina,
    # plantillas, musica y fuentes
    videovina_root = thisParam.get()

    music_dir = videovina_root + '/private/music'
    songs = []
    for _root, _dir, files in os.walk(music_dir):
        for _file in files:
            base_name = _file.split('.')[0]
            name = base_name + '  -  ' + os.path.basename(_root).capitalize()
            songs.append((name, base_name))

    thisNode.getParam('default_song').setOptions(songs)

    fonts_dir = videovina_root + '/private/fonts'
    fonts = []
    if os.path.isdir(fonts_dir):
        for font in os.listdir(fonts_dir):
            base_name = font.split('.')[0]
            fonts.append((base_name, base_name))
    thisNode.getParam('default_font').setOptions(fonts)


def color_if_has_text(thisNode, thisParam):
    if thisParam.get():
        thisNode.setColor(.7, .5, .4)
    else:
        thisNode.setColor(.7, .7, .7)


def set_default_color(thisNode, thisParam):
    current = thisParam.get()
    if current:
        color_param = thisNode.getParam('color_' + str(current))
        if color_param:
            color = color_param.get()
            thisNode.color.set(color[0], color[1], color[2], 1)


def refresh(thisNode, app, workarea):

    speed = thisNode.speed.get()
    _format = thisNode.format.get()
    color = thisNode.color.get()
    speeds = thisNode.speeds.get()

    normal_speed = speeds[1]

    slide_frames = speeds[speed]

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
        speeds_slide = slide.getParam('speeds')
        speed_slide = slide.getParam('speed')

        color_slide.set(color[0], color[1], color[2], color[3])
        speeds_slide.set(speeds[0], speeds[1], speeds[2])
        speed_slide.set(speed)
        format_slide.set(_format)

        start_frame_slide.set(first_frame)

        # Transition
        transition = obj['transition']
        if i == 0:
            # si es la primera transicion deja la transicion en el frame 1
            start_frame = 1
        else:
            start_frame = (last_frame - (transition_frames / 2)) - slide_frames
        transition.getParam('start_frame').set(start_frame)
        transition.getParam('duration').set(transition_frames)
        transition.getParam('format').set(_format)
        transition.getParam('speed').set(speed)
        transition.getParam('speeds').set(speeds[0], speeds[1], speeds[2])
        transition.getParam('refresh').trigger()
        # --------------------

        reformat = obj['reformat']
        if reformat:
            reformat.getParam('boxSize').set(width, hight)
            reformat.getParam('refresh').trigger()

        # si es el primer slide, le sumamos la mitad de la duracion de la transicion,
        # ya que la primera transicion va a negro.
        if i == 0:
            first_frame += slide_frames + mid_transition_frames
        else:
            first_frame += slide_frames
        last_frame += slide_frames

        connect_slide_inputs(slides, i)


def connect_slide_inputs(slides, current_slide):
    # conecta todas las entradas de cada slide, asi
    # poder usarlas dentro del grupo de la slide
    slide = slides[current_slide]['slide']
    extra_count = slide.getMaxInputCount() - 1

    if not extra_count:
        return

    slide_count = len(slides)
    connect_nodes_count = slide_count - 1

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

            reformat = slides[connect_node]['reformat']
            slide.disconnectInput(i)
            slide.connectInput(i, reformat)

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

            reformat = slides[connect_node]['reformat']
            slide.disconnectInput(i)
            slide.connectInput(i, reformat)

            connect_node += 1


def extra_picture_inputs(thisNode, app, workarea):
    amount = thisNode.input_amount.getValue()
    count = thisNode.getMaxInputCount()

    if amount + 1 <= count:
        alert('Ya existen ' + str(amount) + ' inputs extra.', 'Slide inputs')
        return

    posx = 0
    for i in range(amount):
        name = 'E-' + str(i + 1)
        _input = getNode(workarea, name)
        if not _input:
            _input = createNode('input', name, workarea, position=[posx, 0])

        posx += 200


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


def delete_slide(workarea, slide_number):
    # se usa .destroy() 2 veces ya que a veces
    # natron no borra el nodo
    def remove(index):
        obj = get_slide(workarea, index)
        for key, node in obj.iteritems():
            if node:
                if not type(node) == bool:
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
    format_index = thisNode.format.get()
    pixels = formats[format_index]

    return pixels


def generate_black():
    None


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

            slide = app.createNode('vv.slide', 2, workarea)
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
            transition_name = 'vv.' + \
                transition_param.getOption(transition_param.get())
            transition = app.createNode(transition_name, 2, workarea)
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
    update_post_fx(thisNode, app, workarea)
    refresh(thisNode, app, workarea)

    if current_slides:
        alert('Se han creado ' + str(current_slides) +
              ' Slides base.', 'VideoVina')


def get_slide(workarea, index):
    _index = str(index)

    slide = getNode(workarea, 'slide_' + _index)
    reformat = getNode(workarea, 'slide_' + _index + '_reformat')
    image = getNode(workarea, 'slide_' + _index + '_image')
    transition = getNode(workarea, 'slide_' + _index + '_transition')
    dot = getNode(workarea, 'slide_' + _index + '_dot')

    production = False
    # si no no existe la slide base, busca la slide de produccion, si
    # es que all=True
    if not slide:
        slide = getNode(workarea, 'slide_' + _index + 'p')
        reformat = getNode(workarea, 'slide_' + _index + 'p_reformat')
        image = getNode(workarea, 'slide_' + _index + 'p_image')
        transition = getNode(workarea, 'slide_' + _index + 'p_transition')
        dot = getNode(workarea, 'slide_' + _index + 'p_dot')

        production = True
    # --------------------

    return {
        'production': production,
        'slide': slide,
        'reformat': reformat,
        'image': image,
        'transition': transition,
        'dot': dot
    }


def get_slides(workarea, production=True, base=True, separate=False):
    # si 'all' es False obtiene solo las slide de base
    production_list = []
    base_list = []
    all_list = []

    for i in range(100):
        obj = get_slide(workarea, i)
        if obj['slide']:
            all_list.append(obj)
            if obj['production']:
                production_list.append(obj)
            else:
                base_list.append(obj)

    if separate:
        return [base_list, production_list]
    elif production and base:
        return all_list
    elif production:
        return production_list
    elif base:
        return base_list


def update_post_fx(thisNode, app, workarea):
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


def duplicate_slides(thisNode, app, workarea):
    amount = thisNode.production_slides.get()

    generated = generate_production_slides(thisNode, app, workarea, amount)
    if not generated:
        return

    update_post_fx(thisNode, app, workarea)
    generate_random_pictures(thisNode, app, workarea, amount)
    refresh(thisNode, app, workarea)

    alert('Ya se duplicaron las slide de Produccion.',
          'Duplicate from base slides.')


def generate_production_slides(thisNode, app, workarea, amount, force=False, reformat=True):
    # duplica los slides base, dependiendo de la
    # cantidad de fotos que importemos.
    base_amount = thisNode.amount_slide.get()

    base_slides, production_slides = get_slides(workarea, separate=True)
    base_count = len(base_slides)
    slides_count = base_count + len(production_slides)

    if not force:
        if not slides_count:
            warning(
                'Production Slides', 'No hay ninguna slide base creada.')
            return False

        if amount <= base_amount:
            warning(
                'Production Slides', 'La Cantidad de slides tiene que ser mayor que los slides base.')
            return False

        if amount == slides_count:
            warning(
                'Production Slides', 'Ya existen ' + str(amount) + ' slides.')
            return False

    count_delete_slide = None
    if amount <= slides_count:
        count_delete_slide = slides_count - amount
        if not force:
            message = 'La cantidad de slides es menor a la existente, se eliminaran ' + \
                str(count_delete_slide) + ' slides.'
            ok = question('Estas seguro de que quieres continuar ?', message)
            if not ok:
                return False

    if count_delete_slide:
        # borra las slides que sobran
        _range = range(slides_count - count_delete_slide, slides_count)
        delete_slide(workarea, _range)
    else:
        last_transition = None
        last_dot = None

        slide_obj = get_slide(workarea, slides_count - 1)
        last_base_transition = slide_obj['transition']
        last_base_dot = slide_obj['dot']

        current = 0
        posx = (xdistance * slides_count) + xdistance
        for i in range(amount - slides_count):
            index = i + slides_count

            slide = base_slides[current]['slide']
            transition = base_slides[current]['transition']

            if reformat:
                _reformat = base_slides[current]['reformat']

                new_reformat = copy(_reformat, workarea)
                new_reformat.setColor(.4, .5, .7)
                new_reformat.setPosition(posx, -200)
                new_reformat.setLabel('slide_' + str(index) + 'p_reformat')

            new_slide = copy(slide, workarea)
            new_slide.setPosition(posx, 0)
            new_slide.setLabel('slide_' + str(index) + 'p')
            if reformat:
                new_slide.connectInput(0, new_reformat)

            new_transition = copy(transition, workarea)
            new_transition.setColor(.7, .7, .4)
            new_transition.setPosition(posx, 200)
            new_transition.setLabel('slide_' + str(index) + 'p_transition')
            if last_transition:
                new_transition.connectInput(0, last_transition)
            else:
                new_transition.connectInput(0, last_base_transition)

            new_transition.connectInput(1, new_slide)

            dot = app.createNode('fr.inria.built-in.Dot', 2, workarea)
            dot_name = 'slide_' + str(index) + 'p_dot'
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

    return True


def save_production_projects(thisNode):
    print 'save_production'


def export_video_previs(workarea, app, template_name, resources):
    last_transition = getNode(workarea, 'last_transition')

    filename = resources + '/previs.mov'

    render(
        script_name='video_previs_export',
        jobname='Video Previs: ' + template_name,
        filename=filename,
        frame=[1, 210],
        resolution=formats[0],
        node=last_transition,
        parent_node=workarea
    )


def export_sample_frame(workarea, central_frame, resources):
    sample_slide_index = 0
    slide = get_slide(workarea, sample_slide_index)['slide']

    render(
        script_name='export_sample_image',
        jobname='Sample Image: ' + str(sample_slide_index),
        filename=resources + '/image.jpg',
        frame=central_frame,
        resolution=[800, 450],
        node=slide,
        parent_node=workarea
    )


def render(script_name='', jobname='', filename='', frame=1, resolution=[640, 360], node=None, parent_node=None):
    # exporta 1 frame con vinarender
    posx = node.getPosition()[0] + 120
    posy = node.getPosition()[1]

    # cambia resolucion
    reformat_name = 'reformat_' + script_name
    reformat = getNode(parent_node, reformat_name)
    if not reformat:
        reformat = createNode('reformat', reformat_name,
                              parent_node, position=[posx, posy])
        reformat.getParam('reformatType').set(1)
    reformat.getParam('boxSize').set(resolution[0], resolution[1])
    reformat.connectInput(0, node)
    # ----------------------

    vinarender_node = getNode(parent_node, script_name)
    if not vinarender_node:
        vinarender_node = createNode(
            'vinarender', script_name, parent_node, position=[posx, posy + 50])
        vinarender_node.setScriptName(script_name)
        vinarender_node.connectInput(0, reformat)

    if type(frame) == int:
        vinarender_node.getParam('range').set(frame, frame)
    else:
        vinarender_node.getParam('range').set(frame[0], frame[1])

    vinarender_node.getParam('filename').set(filename)
    vinarender_node.getParam('job_name').set(jobname)
    vinarender_node.getParam('instances').set(10)

    vinarender_node.getParam('no_dialog').set(True)
    vinarender_node.getParam('render').trigger()


def export_overlap_frames(workarea, template_name, central_frame, resources):
    slides = get_slides(workarea, production=False)
    overlap = resources + '/overlap'

    if not os.path.isdir(overlap):
        os.makedirs(overlap)

    for i, obj in enumerate(slides):
        slide = obj['slide']

        render(
            script_name='OverlapSlide-' + str(i),
            jobname=template_name + ' - Slide Overlap:  ' + str(i),
            filename=overlap + '/' + slide.getLabel() + '.png',
            frame=central_frame,
            resolution=[640, 360],
            node=slide.getNode('FX'),
            parent_node=slide
        )


def export_videovina_info(thisNode, app, workarea, project_path):

    # obtiene la duracion de las slides
    speed = thisNode.speed.get()
    speeds = thisNode.speeds.get()
    slide_frames = speeds[speed]
    # -----------------

    # deja el proyecto en hd medio para que sea mas rapido cada render
    thisNode.getParam('format').set(1)
    refresh(thisNode, app, workarea)

    # el frame central de la slide
    central_frame = slide_frames / 2

    template_name = app.projectName.get().split('.')[0]
    resources = project_path + '/resources'

    export_default_project(thisNode, app, workarea, project_path)
    export_overlap_frames(workarea, template_name, central_frame, resources)
    export_sample_frame(workarea, central_frame, resources)
    export_video_previs(workarea, app, template_name, resources)

    alert('Ya se enviaron los renders a vinarender para que genere los datos para VideoVina.', 'VideoVina Info.')


def update_videovina_project(thisNode, app, workarea):

    private = thisNode.getParam('videovina_root').get() + '/private'
    project_file = thisNode.getParam('videovina_project').get()
    project = jread(project_file)

    footage = os.path.dirname(project_file) + '/footage'

    # leer datos del proyecto json de videovina
    color = project.states.app.color
    timeline = project.states.app.timeline
    speed = project.states.preview.speed
    song = project.states.app.song
    global_font = project.states.app.font
    # ----------------

    # modifica los datos del proyecto natron
    thisNode.getParam('color').set(
        color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1)
    thisNode.getParam('speed').set(speed)
    # ------------------

    photos = []
    count = len(timeline)
    for photo in timeline:
        basename = photo.name.split('.')[0]
        url = footage + '/' + basename + '.jpg'
        photos.append(url)

    generate_production_slides(
        thisNode, app, workarea, count, force=True, reformat=False)

    def font_path(font_name):
        font_path = private + '/fonts/' + font_name + '.'
        _font = font_path + 'otf'
        if not os.path.isfile(_font):
            _font = font_path + 'ttf'

        return _font

    thisNode.getParam('font').set(font_path(global_font))

    # cambia los titulos de todas las slides
    for i, obj in enumerate(get_slides(workarea)):
        slide = obj['slide']

        item = timeline[i]

        if item.separate_font:
            slide.getParam('font').set(font_path(item.font))
        else:
            slide.getParam('font').set(font_path(global_font))

        if item.text:
            include_texts = slide.getParam('include_texts')
            include_texts.set(0)
            include_texts.set(item.text_enabled)

            if item.text_enabled:
                slide.getParam('title').set(item.title)
                slide.getParam('subtitle').set(item.subtitle)
            else:
                slide.getParam('title').set('')
                slide.getParam('subtitle').set('')
    # -----------------------------

    # song
    song_type = get_type_song(thisNode, song)
    song_path = private + '/music/' + song_type + '/' + song + '.mp3'
    thisNode.getParam('song').set(song_path)
    # -------------

    generate_pictures(workarea, app, photos)
    update_post_fx(thisNode, app, workarea)
    refresh(thisNode, app, workarea)


def export_default_project(thisNode, app, workarea, project_path):
    project_name = app.projectName.get().split('.')[0]
    videovina_root = thisNode.getParam('videovina_root').get()

    base_project = videovina_root + '/misc/base_project.json'
    resources = project_path + '/resources'
    out_project = resources + '/project.json'

    if not os.path.isdir(resources):
        os.makedirs(resources)

    project = jread(base_project)

    # obtiene colores de muestra
    colors = []
    for i in range(1, 4):
        _color = thisNode.getParam('color_' + str(i)).get()
        color = [_color[0] * 255, _color[1] * 255, _color[2] * 255]
        colors.append(color)

    project.states.color.basic_colors = colors
    # ----------------

    # datos de los textos:
    base_slides, production_slides = get_slides(workarea, separate=True)
    base_count = len(base_slides)

    slides_base = []
    for i, obj in enumerate(base_slides):
        slide = obj['slide']

        transform = slide.getNode('Transform')
        _transform = {
            'rotate': transform.getParam('rotate').get(),
            'scale': transform.getParam('scale').getValue(),
            'x': transform.getParam('translate').get()[0],
            'y': transform.getParam('translate').get()[1]
        }

        include_texts = slide.getParam('include_texts').get()

        item = {
            'foreground': 'overlap/slide_' + str(i) + '.png',
            'text': include_texts,
            'transform': _transform
        }
        slides_base.append(item)
    # ----------------------

    # font
    default_font = thisNode.getParam('default_font')
    font = default_font.getOption(default_font.get())
    # --------------

    project.states.timeline.slides_base = slides_base
    project.states.timeline.slides_base_count = base_count
    project.states.app.font = font

    frame_rate = 30.0
    speeds = thisNode.getParam('speeds').get()
    transition = thisNode.getParam('transition_duration').get() / frame_rate
    project.states.preview.transition_duration = [
        (transition * speeds[0]) / 100,
        (transition * speeds[1]) / 100,
        (transition * speeds[2]) / 100
    ]
    project.states.preview.speeds = [
        speeds[0] / frame_rate,
        speeds[1] / frame_rate,
        speeds[2] / frame_rate
    ]

    # song
    song_name = get_current_song(thisNode)[0]
    project.states.app.song = song_name
    project.states.music.playing = song_name
    # --------------

    # cambia el tipo
    project.type = project_name
    # -------------

    jwrite(out_project, project)

    alert('Proyecto ya fue exportado.', 'Export default project')


def transfer_to_static(thisNode, app, project_path):

    template_name = app.projectName.get().split('.')[0]
    static_templates = thisNode.getParam(
        'videovina_root').get() + '/static/templates/' + template_name
    resources = project_path + '/resources'

    if not os.path.isdir(static_templates):
        os.makedirs(static_templates)

    # copia la json de informacion de la plantilla
    info = resources + '/info.json'
    shutil.copy(info, static_templates)
    # -------------------------

    # convertir la imagen renderizada a un formato jpg mas liviano
    os.system('ffmpeg -y -i "' + resources +
              '/image.jpg" -q:v 10 "' + static_templates + '/image.jpg"')

    # convertir el previs renderizada a un formato mp4 mas liviano
    os.system('ffmpeg -y -i "' + resources +
              '/previs.mov" -b 500k "' + static_templates + '/previs.mp4"')

    # copia la carpeta overlap
    static_overlap = static_templates + '/overlap'
    if os.path.isdir(static_overlap):
        shutil.rmtree(static_overlap)
    shutil.copytree(resources + '/overlap', static_overlap)

    # copia proyecto
    shutil.copy(resources + '/project.json', static_templates)

    alert('Se transfirieron todos los archivos a la carpeta estatica de videovina.')
