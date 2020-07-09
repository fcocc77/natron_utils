from general import formats
from natron_extent import question, run
from slides import get_slides


def clean(thisNode, workarea):
    if question("Esta seguro que desea aligerar todos las slides ?", 'Limpiar Slides'):
        for slide in get_slides(workarea):
            transition = slide['transition']
            run(transition, 'clean', (transition, False))


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


def get_resolution(thisNode):
    # obtiene la correcta resolucion a partir de una escala
    # tomando como referencia el 1920x1080
    format_index = thisNode.format.get()
    pixels = formats[format_index]

    return pixels
