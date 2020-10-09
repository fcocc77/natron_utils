from general import formats
from nx import question, trigger
from slides import get_slides


def clean(thisNode, workarea):
    if question("Esta seguro que desea aligerar todos las slides ?", 'Limpiar Slides'):
        for slide in get_slides(workarea):
            slide_clean = slide['slide'].getParam('clean')
            if slide_clean:
                trigger(slide_clean)

            transition_clean = slide['transition'].getParam('clean')
            if transition_clean:
                trigger(transition_clean)


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


def get_resolution(thisNode):
    # obtiene la correcta resolucion a partir de una escala
    # tomando como referencia el 1920x1080
    format_index = thisNode.getParam('format').get()
    pixels = formats[format_index]

    return pixels
