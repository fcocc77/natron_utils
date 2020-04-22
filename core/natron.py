from util import *


def createParam(node, name, _type=None, _range=[0, 100]):
    # funcion para crear parametros mas facilmente

    label = name.replace('_', ' ').title()

    # creacion de parametro
    if _type == 'float':
        param = node.createDoubleParam(name + '_param', label)
    elif _type == 'int':
        param = node.createIntParam(name + '_param', label)
    elif _type == 'string':
        param = node.createStringParam(name + '_param', label)
    elif name == 'separator':
        param = node.createSeparatorParam("sep_" + hash_generator(5), "")
    elif _type == 'button':
        param = node.createButtonParam(name + '_param', label)
    elif _type == 'choice':
        param = node.createChoiceParam(name + '_param', label)
    elif _type == 'label':
        param = node.createSeparatorParam(name + '_param', label)

    # establece el rango de la slide
    allowed = ['float', 'int']
    if _type in allowed:
        param.setMinimum(_range[0], 0)
        param.setMaximum(_range[1], 0)
        param.setDisplayMinimum(_range[0], 0)
        param.setDisplayMaximum(_range[1], 0)
    # ----------------------

    # agrega el parametro a la pestania
    node.controls.addParam(param)
    # ----------------------

    return param
