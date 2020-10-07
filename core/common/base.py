from nx import alert, warning, getNode, restore_default, question, get_connected_nodes, node_delete, get_nodes_by_type
from vina import get_videovina
from general import formats, rscale
import NatronEngine
try:
    import NatronGui
except:
    None


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)


def clean(thisNode, force=False):
    # elimina todos los nodos que solo se usan para el desarrollo, dejando los nodos necesarios

    def action():
        twelve_render_nodes = get_nodes_by_type(thisNode, 'vv.TwelveRender')

        nodes = []
        for twelve_render in twelve_render_nodes:
            for node in get_connected_nodes(twelve_render):
                if not node.getPluginID() == 'fr.inria.built-in.Input':
                    nodes.append(node)

        node_delete(nodes)

    if force:
        action()
    else:
        if question("Esta seguro que desea borrar los nodos de desarollo ?", 'Limpiar Nodos'):
            action()


def link_to_parent(thisNode, thisParam, thisGroup, force=False):
    # vincula algunos parametros al nodo padre
    if not force:
        if not thisParam.getScriptName() == 'link':
            return

    # si el grupo es el root 'app', hace la vinculacion al nodo de videovina
    node_for_expression = 'thisGroup'
    if type(thisGroup) == NatronGui.GuiApp:
        videovina_node = get_videovina()

        if not videovina_node:
            return
        node_for_expression = videovina_node.getScriptName()
        thisGroup = videovina_node

    params_count = 0

    def allow(param):
        blacklist_params = [
            NatronEngine.ButtonParam,
            NatronEngine.PageParam
        ]
        param_type = type(param)

        if param_type in blacklist_params:
            return False

        if param_type == NatronEngine.StringParam:
            if not param.getLabel():
                return False

        return True

    def link(attribute):
        attribute_parent = thisGroup.getParam(attribute)
        attribute_child = thisNode.getParam(attribute)
        if attribute_child and attribute_parent:
            if allow(attribute_child):
                if hasattr(attribute_parent, 'setAsAlias'):
                    restore_default(attribute_child)
                    attribute_parent.setAsAlias(attribute_child)

                    return 1
        return 0

    for param in thisNode.getParams():
        page = param.getParent()
        if page:
            if page.getScriptName() == 'control':
                params_count += link(param.getScriptName())

    if not force:
        if params_count > 0:
            alert('Se vincularon ' + str(params_count) + ' parametros.')
        else:
            warning('Link Error', 'El nodo padre no tiene los atributos para vincularlo')


def children_refresh(thisParam, thisNode):
    # actualiza todos los nodos hijos, si presionamos el boton refresh,
    # y si es que el nodo hijo tiene el parametro de 'refresh'
    if not thisParam:
        return

    if thisParam.getScriptName() == 'refresh':
        for node in thisNode.getChildren():
            refresh = node.getParam('refresh')
            if refresh:
                refresh_expressions(thisNode)
                refresh.trigger()


def refresh_expressions(node):
    # A veces queda las expression con error, cuando cambiamos nombre u otra razon,
    # con esta funcion actualiazamos las expressiones

    for param in node.getParams():
        if hasattr(param, "getExpression"):
            for dimension in range(param.getNumDimensions()):
                exp, hasRetVariable = param.getExpression(dimension)
                if exp:
                    param.setExpression(exp, hasRetVariable)

    for child in node.getChildren():
        refresh_expressions(child)


def get_durations(node):
    durations_param = node.getParam('durations')

    if not durations_param:
        return None

    return durations_param.get()


def get_duration(node, base=False):
    speed_param = node.getParam('speed')
    duration_percent_param = node.getParam('duration_percent')

    if not speed_param:
        return None

    if duration_percent_param:
        duration_percent = duration_percent_param.get()
    else:
        duration_percent = 100

    duration = get_durations(node)[speed_param.get()]

    if base:
        return duration

    return duration_percent * duration / 100


def get_transition_duration(node):
    transition_duration_param = node.transition_duration.get()

    if not transition_duration_param:
        return

    duration = get_duration(node)

    transition_duration = (duration / 2) * transition_duration_param / 100

    return transition_duration


def get_start_frame(node):
    speed_param = node.getParam('speed')
    duration_percent_param = node.getParam('duration_percent')

    if duration_percent_param:
        duration_percent = duration_percent_param.get()
    else:
        duration_percent = 100

    duration = get_durations(node)[speed_param.get()]
    duration -= get_duration(node)

    start_frame = duration / 2

    return start_frame + 1


def get_format(node):
    format_param = node.getParam('format')

    if not format_param:
        return None

    return formats[format_param.get()]


def get_rscale(node):
    format_param = node.getParam('format')

    if not format_param:
        return None

    return rscale[format_param.get()]


def reformat_update(node, reformat):
    # actualiza un reformat al actual resolucion del nodo

    if type(reformat) == str:
        reformat = getNode(node, reformat)

    if not reformat:
        return

    current_format = get_format(node)

    reformat.getParam('reformatType').set(1)
    reformat.getParam('boxSize').set(current_format[0], current_format[1])


def limit_transition(node):
    # limita con un switch llamado 'limit', el fx de la transicion,
    # para que no cargue mas alla de la duracion de la transicion.

    switch_param = getNode(node, 'limit')

    if not switch_param:
        return

    switch = switch_param.getParam('which')

    duration = get_duration(node)
    start_frame = get_start_frame(node) - 1
    last_frame = start_frame + duration

    switch.restoreDefaultValue()

    switch.setValueAtTime(0, start_frame)
    switch.setValueAtTime(1, start_frame + 1)

    switch.setValueAtTime(1, last_frame)
    switch.setValueAtTime(2, last_frame + 1)
