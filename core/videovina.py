import random
import os
import NatronGui
from natron_utils import copy, getNode, question, alert, createNode
from transition import directional_transition
from util import jread, jwrite

# separacion de los nodos en horizontal
xdistance = 200
# ----------------

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_slides':
        generate_base_slides(thisNode, app)
    elif knob_name == 'save_production':
        save_production_projects(thisNode)
    elif knob_name == 'refresh':
        refresh(thisNode, app)
    elif knob_name == 'generate_inputs':
        extra_picture_inputs(thisNode, app)
    elif knob_name == 'duplicate_slides':
        duplicate_slides(thisNode, app)
    elif knob_name == 'videovina_info':
        videovina_info(thisNode, app)
    elif knob_name == 'update_videovina_project':
        update_videovina_project(thisNode, app)
    elif knob_name == 'export_default_project':
        export_default_project(thisNode, app)
    elif knob_name == 'default_color':
        set_default_color(thisNode, thisParam)
    elif knob_name == 'include_texts':
        color_if_has_text(thisNode, thisParam)

def color_if_has_text(thisNode, thisParam):
    if thisParam.get():
        thisNode.setColor(.7, .5, .4)
    else:
        thisNode.setColor(.7, .7, .7)

def set_default_color(thisNode, thisParam):
    current = thisParam.get()
    if current:
        color_param = thisNode.getParam('color_' + str( current ))
        if color_param:
            color = color_param.get()
            thisNode.color.set(color[0], color[1], color[2], 1)

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
    if not first_black:
        return
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
        frame_range = slide.getParam('frameRange')
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
        connect_node = current_slide - ( extra_count / 2 )
        
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

def extra_picture_inputs(thisNode, app):
    amount = thisNode.input_amount.getValue()
    count = thisNode.getMaxInputCount()

    if amount + 1 <= count:
        alert('Ya existen ' + str(amount) + ' inputs extra.', 'Slide inputs')
        return

    posx = 0
    for i in range(amount):
        name = 'E-' + str(i + 1)
        _input = getNode(thisNode, name)
        if not _input:
            _input = createNode('input', name, thisNode, position=[posx, 0])

        posx += 200

def generate_random_pictures(thisNode, app, amount):
    
    references_dir = thisNode.reference_pictures.get()
    references_pictures = os.listdir( references_dir )
    references_count = len( references_pictures )

    index = random.randint(0, references_count - 1)

    random_pictures = []
    for i in range(amount):
        picture = references_dir + '/' + references_pictures[index]
        random_pictures.append(picture)

        index += 1
        if index >= references_count:
            index = 0 

    generate_pictures(thisNode, app, random_pictures)

def generate_pictures(thisNode, app, pictures):
    for i, obj in enumerate( get_slides(thisNode) ):
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
            reader = app.createReader( picture, thisNode )
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

def delete_slide(thisNode, slide_number):
    # se usa .destroy() 2 veces ya que a veces
    # natron no borra el nodo
    def remove(index):
        obj = get_slide(thisNode, index)
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
    rscale = thisNode.rscale.get()

    width = 1920 * rscale
    hight = 1080 * rscale

    return [width, hight]

def generate_black():
    None

def generate_base_slides(thisNode, app):
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
    
    current_slides = 0

    if count_delete_slide: 
        # borra las slides que sobran
        _range = range(slides_count - count_delete_slide, slides_count)
        delete_slide(thisNode, _range)
        # -----------------------

        current_slides = slides_count - count_delete_slide
    else:
        width, hight = get_resolution(thisNode)
        posx = 0 - xdistance
        last_transition = getNode(thisNode, 'slide_' + str( slides_count - 1 ) + '_transition')
        last_dot = getNode(thisNode, 'slide_' + str( slides_count - 1 ) + '_dot')
        
        for i in range(count):
            posx += xdistance

            # si la slide ya fue generada, omite la creacion de la slide y pasa a la siguiente
            if slides_count - 1 >= i:
                continue
            # -------------------
            current_slides += 1

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

    generate_random_pictures(thisNode, app, current_slides + slides_count)
    update_post_fx(thisNode, app)
    refresh(thisNode, app)

    if current_slides:
        NatronGui.natron.informationDialog('VideoVina', 'Se han creado ' + str(current_slides) + ' Slides base.')
     
def get_slide(thisNode, index):
    _index = str(index)

    slide = getNode(thisNode, 'slide_' + _index)    
    reformat = getNode(thisNode, 'slide_' + _index + '_reformat')
    image = getNode(thisNode, 'slide_' + _index + '_image')
    transition = getNode(thisNode, 'slide_' + _index + '_transition')
    dot = getNode(thisNode, 'slide_' + _index + '_dot')

    production = False
    # si no no existe la slide base, busca la slide de produccion, si
    # es que all=True
    if not slide:
        slide = getNode(thisNode, 'slide_' + _index + 'p')    
        reformat = getNode(thisNode, 'slide_' + _index + 'p_reformat')
        image = getNode(thisNode, 'slide_' + _index + 'p_image')
        transition = getNode(thisNode, 'slide_' + _index + 'p_transition')
        dot = getNode(thisNode, 'slide_' + _index + 'p_dot')

        production = True
    # --------------------

    return {
        'production' : production, 
        'slide' : slide,
        'reformat' : reformat,
        'image' : image,
        'transition' : transition,
        'dot' : dot
    }

def get_slides(thisNode, production = True, base = True, separate = False):
    # si 'all' es False obtiene solo las slide de base
    production_list = []
    base_list = []
    all_list = []

    for i in range(100):        
        obj = get_slide(thisNode, i)
        if obj['slide']:
            all_list.append(obj)
            if obj['production']:
                production_list.append(obj)
            else:
                base_list.append(obj)

    if separate:
        return [ base_list, production_list ]
    elif production and base:
        return all_list
    elif production:
        return production_list
    elif base:
        return base_list

def update_post_fx(thisNode, app):
    slides = get_slides(thisNode)
    if not len(slides):
        return    

    # obtiene el primer y el ultimo nodo de transition
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
        first_constant.getParam('color').set(0,0,0,1)
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
        last_constant.getParam('color').set(0,0,0,1)
    last_constant.setPosition( last_posx + 200, 100 )
    # ---------------------

    # la ultima transition es un dissolve
    dissolve = getNode(thisNode, 'last_transition')
    if not dissolve:
        dissolve = createNode(
            'dissolve', 
            'last_transition', 
            thisNode,
            color=[.4, .5, .4]
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
    post_fx_dot.setPosition(last_posx + 243, 900)
    post_fx_dot.disconnectInput(0)
    post_fx_dot.connectInput(0, dissolve)    

    # output
    output = getNode(thisNode, 'Output1')    
    if not output:
        output = createNode('output' , 'Output1', thisNode)
    output.setPosition(last_posx + 200, 1100)
    output.connectInput(0, post_fx_dot)    

    # si es que existe un viewer lo posiciona correctamente
    viewer = None
    for i in range(10):
        viewer = thisNode.getNode('Viewer' + str(i))
        if viewer:
            viewer.setPosition(last_posx + 450, 895)
            viewer.disconnectInput(0)
            viewer.connectInput(0, post_fx_dot)  
            break   
    # ---------------------

def duplicate_slides(thisNode, app):
    amount = thisNode.production_slides.get()
    
    generated = generate_production_slides(thisNode, app, amount)
    if not generated:
        return

    update_post_fx(thisNode, app)
    generate_random_pictures(thisNode, app, amount)
    refresh(thisNode, app)

    alert('Ya se duplicaron las slide de Produccion.','Duplicate from base slides.')

def generate_production_slides(thisNode, app, amount, force = False, reformat = True):
    # duplica los slides base, dependiendo de la
    # cantidad de fotos que importemos.
    base_amount = thisNode.amount_slide.get()
        
    base_slides, production_slides = get_slides(thisNode, separate = True)
    base_count = len( base_slides )
    slides_count = base_count + len( production_slides )

    if not force:
        if not slides_count:
            NatronGui.natron.warningDialog( 'Production Slides', 'No hay ninguna slide base creada.' )
            return False

        if amount <= base_amount: 
            NatronGui.natron.warningDialog( 'Production Slides', 'La Cantidad de slides tiene que ser mayor que los slides base.' )
            return False
        
        if amount == slides_count:
            NatronGui.natron.warningDialog( 'Production Slides', 'Ya existen ' + str(amount) + ' slides.' )
            return False

    count_delete_slide = None
    if amount <= slides_count:
        count_delete_slide = slides_count - amount
        if not force:
            message = 'La cantidad de slides es menor a la existente, se eliminaran ' + str(count_delete_slide) + ' slides.'
            ok = question('Estas seguro de que quieres continuar ?', message) 
            if not ok:
                return False

    if count_delete_slide:
        # borra las slides que sobran
        _range = range(slides_count - count_delete_slide, slides_count)
        delete_slide(thisNode, _range)
    else:
        last_transition = None
        last_dot = None

        slide_obj = get_slide(thisNode, slides_count - 1)
        last_base_transition = slide_obj['transition']
        last_base_dot = slide_obj['dot']

        current = 0
        posx = ( xdistance * slides_count ) + xdistance
        for i in range( amount - slides_count ):
            index = i + slides_count
            
            slide = base_slides[current]['slide']
            transition = base_slides[current]['transition']
            
            if reformat:
                _reformat = base_slides[current]['reformat']

                new_reformat = copy(_reformat, thisNode)
                new_reformat.setColor(.4, .5, .7)
                new_reformat.setPosition(posx, -200)
                new_reformat.setLabel('slide_' + str(index) + 'p_reformat')

            new_slide = copy(slide, thisNode)
            new_slide.setPosition(posx, 0)
            new_slide.setLabel('slide_' + str(index) + 'p')
            if reformat:
                new_slide.connectInput(0, new_reformat)

            new_transition = copy(transition, thisNode)
            new_transition.setColor(.7, .7, .4)
            new_transition.setPosition(posx, 200)
            new_transition.setLabel('slide_' + str(index) + 'p_transition')
            if last_transition:
                new_transition.connectInput(0, last_transition)
            else:
                new_transition.connectInput(0, last_base_transition)

            new_transition.connectInput(1, new_slide)

            dot = app.createNode('fr.inria.built-in.Dot', 2, thisNode)
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

def videovina_info(thisNode, app):

    slides = get_slides(thisNode, production = False)
    
    # obtiene la duracion de las slides
    velocity = thisNode.velocity.get()
    speeds = thisNode.speeds.get()
    slide_frames = speeds[ velocity ]
    # -----------------

    project_path = os.path.dirname( os.path.dirname( app.getProjectParam('projectPath').get() ) )
    resources = project_path + '/resources/overlap'
    if not os.path.isdir(resources):
        os.makedirs(resources)

    # el frame central de la slide
    central_frame = slide_frames / 2

    for i, obj in enumerate(slides):
        slide = obj['slide']
        fx = slide.getNode('FX')

        posx = fx.getPosition()[0] + 200
        posy = fx.getPosition()[1]

        render_name = 'OverlapSlide-' + str(i)
        vinarender_node = getNode(slide, render_name)
        if not vinarender_node:
            vinarender_node = createNode('vinarender', render_name, slide, position = [posx, posy])
            vinarender_node.connectInput(0, fx)

        vinarender_node.getParam('range').set(central_frame, central_frame)
        

        _file = resources + '/' + slide.getLabel() + '.png'
        vinarender_node.getParam('filename').set(_file)
        jobname = app.projectName.get() + ' - Slide Overlap:  ' + str(i) 
        vinarender_node.getParam('job_name').set(jobname)
        vinarender_node.getParam('instances').set(10)

        vinarender_node.getParam('no_dialog').set(True)
        vinarender_node.getParam('render').trigger()
        vinarender_node.getParam('no_dialog').set(False)


    alert('Ya se enviaron los renders a vinarender para que genere los datos para VideoVina.','VideoVina Info.')

def update_videovina_project(thisNode, app):

    project_file = thisNode.getParam('videovina_project').get()
    project = jread(project_file)

    footage = os.path.dirname(project_file) + '/footage'

    # leer datos del proyecto json de videovina
    color = project.states.app.color
    timeline = project.states.app.timeline
    velocity = project.states.edit.duration
    texts = project.states.edit_items
    # ----------------

    # modifica los datos del proyecto natron 
    thisNode.getParam('color').set( color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1)
    thisNode.getParam('velocity').set(velocity)
    # ------------------

    photos = []
    count = len(timeline)
    for photo in timeline:
        basename = photo.name.split('.')[0]
        url = footage + '/' + basename + '.jpg'
        photos.append(url)

    generate_production_slides(thisNode, app, count, force=True, reformat=False)

    # cambia los titulos de todas las slides
    for i, obj in enumerate( get_slides(thisNode) ):
        slide = obj['slide']

        text_name = 'text' + str(i + 1)
        
        if hasattr(texts, text_name):
            text = getattr(texts, text_name)
            include_texts = slide.getParam('include_texts')
            include_texts.set(0)
            include_texts.set(text.enable)
            
            if text.enable:
                slide.getParam('title').set(text.title)
                slide.getParam('subtitle').set(text.subtitle)
            else:
                slide.getParam('title').set('')
                slide.getParam('subtitle').set('')

    # -----------------------------
    
    generate_pictures(thisNode, app, photos)
    update_post_fx(thisNode, app)
    refresh(thisNode, app)

def export_default_project(thisNode, app):
    project_path = os.path.dirname( os.path.dirname( app.getProjectParam('projectPath').get() ) )
    base_project = project_path + '/resources/project.json'
    out_project = thisNode.default_json_project.get()
    
    project = jread(out_project)

    # obtiene colores de muestra
    colors = []
    for i in range(1, 4):
        _color = thisNode.getParam('color_' + str(i) ).get()
        color = [ _color[0] * 255, _color[1] * 255, _color[2] * 255 ]
        colors.append(color)
    
    project.states.color.basic_colors = colors
    # ---------------- 

    # datos de los textos: 
    base_slides, production_slides = get_slides(thisNode, separate = True)
    base_count = len( base_slides )

    texts = {}
    texts_indexs = []
    for i, obj in enumerate(base_slides):
        slide = obj['slide']

        transform = slide.getNode('Transform')
        _transform = {
            'rotate' : transform.getParam('rotate').get(),
            'scale' : transform.getParam('scale').getValue(),
            'x' : transform.getParam('translate').get()[0],
            'y' : transform.getParam('translate').get()[1]
        }

        include_texts = slide.getParam('include_texts').get()
        if include_texts:
            index = i + 1
            texts_indexs.append(index)
            name = 'text' + str(index)

            item = {
                'background' : '',
                'foreground' : '',
                'enable' : False,
                'expanded' : False,
                'title' : '',
                'subtitle' : '',
                'transform' : _transform
            }
            texts[name] = item

    project.states.edit.texts = texts
    project.states.edit_items = texts
    project.states.edit.base_slides = base_count
    # ----------------------

    jwrite(out_project, project)

    alert('Proyecto ya fue exportado.', 'Export default project')