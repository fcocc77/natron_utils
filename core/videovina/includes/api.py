# Este archivo contiene todas las funciones para conectar
# el proyecto .json del editor de la pagina de videovina
# al nodo videovina de Natron, datos de entrada y salida.
import os
import shutil
from argparse import Namespace
from util import jread
from develop import refresh, update_post_fx
from pictures import generate_pictures, get_max_pictures
from slides import get_slides, get_slide
from song import get_current_song, get_type_song
from util import jwrite
from nx import alert, getNode, createNode, get_node_by_label
from general import formats
from production import generate_production_slides


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

    local_folder = videovina_root + '/tmp/renders'
    assert_dir = videovina_root + '/private'

    thisNode.getParam('local_renders_folder').set(local_folder)
    thisNode.getParam('assets').set(assert_dir)


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

    vinarender_node = get_node_by_label(script_name, parent_node)
    if not vinarender_node:
        vinarender_node = createNode(
            'vinarender', script_name, parent_node, position=[posx, posy + 50])
        vinarender_node.setLabel(script_name)
        vinarender_node.connectInput(0, reformat)
        vinarender_node.getParam('no_show_message').set(True)

    if type(frame) == int:
        vinarender_node.getParam('range').set(frame, frame)
    else:
        vinarender_node.getParam('range').set(frame[0], frame[1])

    vinarender_node.getParam('filename').set(filename)
    vinarender_node.getParam('job_name').set(jobname)
    vinarender_node.getParam('instances').set(10)

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
    durations = thisNode.durations.get()
    slide_frames = durations[speed]
    # -----------------

    # deja el proyecto en hd medio para que sea mas rapido cada render
    thisNode.getParam('format').set(1)
    refresh()

    # el frame central de la slide
    central_frame = slide_frames / 2

    template_name = app.projectName.get().split('.')[0]
    resources = project_path + '/resources'

    export_default_project(thisNode, app, workarea, project_path)
    export_overlap_frames(workarea, template_name, central_frame, resources)
    export_sample_frame(workarea, central_frame, resources)
    export_video_previs(workarea, app, template_name, resources)

    alert('Ya se enviaron los renders a vinarender para que genere los datos para VideoVina.', 'VideoVina Info.')


def get_videovina_project(videovina_node):
    if not videovina_node.getPluginID() == 'vv.VideoVina':
        return None

    project_file = videovina_node.getParam('videovina_project').get()
    project = jread(project_file)

    footage = os.path.dirname(project_file) + '/footage'

    # el formato en el proyecto, solo se inserta en el modulo api,
    # asi que cuando se esta en desarrollo no aparece, y queda
    # en '2' por defecto que es full hd.
    if hasattr(project, 'format'):
        _format = project.format
    else:
        _format = 2

    if hasattr(project, 'user_id'):
        user_id = project.user_id
    else:
        user_id = ''

    # leer datos del proyecto json de videovina
    return Namespace(
        user=project.user,
        user_id=user_id,
        name=project.name,
        color=project.states.app.color,
        timeline=project.states.app.timeline,
        photos_amount=len(project.states.app.timeline),
        speed=project.states.preview.speed,
        song=project.states.app.song,
        user_songs=project.states.music.user_songs,
        global_font=project.states.app.font,
        user_fonts=project.states.timeline.custom_fonts,
        footage=footage,
        format=_format
    )


def update_videovina_project(videovina_node, app, workarea):
    private = videovina_node.getParam('assets').get()
    local_renders = videovina_node.getParam('local_renders_folder').get()
    pj = get_videovina_project(videovina_node)

    # modifica los datos del proyecto natron
    videovina_node.getParam('color').set(
        pj.color[0] / 255.0, pj.color[1] / 255.0, pj.color[2] / 255.0, 1)
    videovina_node.getParam('speed').set(pj.speed)
    # ------------------

    videovina_node.getParam('total_slides').set(pj.photos_amount)
    videovina_node.getParam('user').set(pj.user)
    videovina_node.getParam('project_name').set(pj.name)
    videovina_node.getParam('user_id').set(pj.user_id)

    photos = []
    count = pj.photos_amount
    first_slide = 0
    last_slide = count - 1

    for photo in pj.timeline:
        basename = photo.name.split('.')[0]
        url = pj.footage + '/' + basename + '.jpg'
        photos.append(url)

    def font_path(font_name):
        # detecta si la fuente es del usuario o de los assets
        user_font = False
        for ufont in pj.user_fonts:
            if ufont.basename == font_name:
                user_font = True
                break
        # --------------------------

        if user_font:
            _font_path = local_renders + '/fonts/' + font_name + '.'
        else:
            _font_path = private + '/fonts/' + font_name + '.'

        _font = _font_path + 'otf'
        if not os.path.isfile(_font):
            _font = _font_path + 'ttf'

        return _font

    videovina_node.getParam('font').set(font_path(pj.global_font))

    # cambia los titulos de todas las slides
    for obj in get_slides(workarea):
        slide = obj['slide']
        index = obj['index']

        if index >= count:
            continue

        item = pj.timeline[index].texts

        if item.separate_font:
            slide.getParam('font').set(font_path(item.font))
        else:
            slide.getParam('font').set(font_path(pj.global_font))

        if item.text:
            include_text = slide.getParam('include_text')
            include_text.set(0)
            include_text.set(item.text_enabled)

            if item.text_enabled:
                slide.getParam('title').set(item.title)
                slide.getParam('subtitle').set(item.subtitle)
            else:
                slide.getParam('title').set('')
                slide.getParam('subtitle').set('')
    # -----------------------------

    # song
    user_song = False
    for usong in pj.user_songs:
        if usong.name == pj.song:
            user_song = True
            break

    if user_song:
        song_path = local_renders + '/' + pj.user + '/' + pj.name + '/' + pj.song + '.mp3'
    else:
        song_type = get_type_song(videovina_node, pj.song)
        song_path = private + '/music/' + song_type + '/' + pj.song + '.mp3'

    videovina_node.getParam('song').set(song_path)
    # -------------

    # format
    videovina_node.getParam('format').set(pj.format)

    generate_pictures(photos, pictures_amount=True, reformat_node=False)
    refresh()


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

        include_texts = slide.getParam('include_text').get()

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
    durations = thisNode.getParam('durations').get()
    transition = thisNode.getParam('transition_duration').get() / frame_rate
    transition_duration = [
        (transition * durations[0]) / 100,
        (transition * durations[1]) / 100,
        (transition * durations[2]) / 100
    ]
    project.states.preview.transition_duration = transition_duration

    project.states.preview.durations = [
        (durations[0] / frame_rate) + (transition_duration[0] / 2),
        (durations[1] / frame_rate) + (transition_duration[1] / 2),
        (durations[2] / frame_rate) + (transition_duration[2] / 2)
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
