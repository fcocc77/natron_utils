# ----------------------------
# extencion de herramientas para Natron
# ----------------------------
from util import *
import NatronEngine
from PySide.QtGui import QMessageBox
from argparse import Namespace
try:
    import NatronGui
except:
    None

_app = None


def app():
    if _app:
        return _app

    try:
        return NatronGui.natron.getGuiInstance(0)
    except:
        return NatronEngine.natron.getActiveInstance()


def is_gui():
    try:
        return NatronGui
    except:
        return False


gui = is_gui()
_disable_dialog = False


def disable_dialog(disable):
    # si 'disable' es True, los dialogos 'alert', 'warning' y 'question' quedan desabilitados,
    # y el dialogo 'question' retorna siempre 'True'
    global _disable_dialog
    _disable_dialog = disable


def trigger(buttom, dialog=False):
    # llama a un buttom con 'trigger' pero sin dialogos si es que los tiene.
    if not dialog:
        disable_dialog(True)
        buttom.trigger()
        disable_dialog(False)
    else:
        buttom.trigger()


def copy(node, group=None):
    _app = app()
    _id = node.getPluginID()

    # si el nodo es un grupo, busca cada parametro en el nodo de origen
    # y lo crea en el nuevo nodo grupo, y luega copia cada nodo hijo con sus atributos
    if _id == 'fr.inria.built-in.Group':
        new_node = _app.createNode('vv.group', 1, group)
        new_node.setScriptName(node.getScriptName())

        new_node.control = new_node.createPageParam("control", "Control")
        new_node.setPagesOrder(['control', 'Node', 'Settings'])

        for p in node.getParams():
            name = p.getScriptName()
            label = p.getLabel()
            _type = type(p)
            param = None
            parent = p.getParent()

            page = None
            if parent:
                page = parent.getScriptName()

            if page == 'Node':
                param = new_node.getParam(name)
            else:
                # identifica que tipo de parametro es, para poder crearlo en el nuevo nodo
                if _type == NatronEngine.BooleanParam:
                    param = new_node.createBooleanParam(name, label)

                elif _type == NatronEngine.ButtonParam:
                    param = new_node.createButtonParam(name, label)

                elif _type == NatronEngine.ChoiceParam:
                    param = new_node.createChoiceParam(name, label)
                    options = []
                    for o in p.getOptions():
                        options.append((o, None))
                    param.setOptions(options)

                elif _type == NatronEngine.ColorParam:
                    useAlpha = False
                    param = new_node.createColorParam(name, label, useAlpha)

                elif _type == NatronEngine.Double2DParam:
                    param = new_node.createDouble2DParam(name, label)

                elif _type == NatronEngine.Double3DParam:
                    param = new_node.createDouble3DParam(name, label)

                elif _type == NatronEngine.DoubleParam:
                    param = new_node.createDoubleParam(name, label)

                elif _type == NatronEngine.FileParam:
                    param = new_node.createFileParam(name, label)

                elif _type == NatronEngine.GroupParam:
                    param = new_node.createGroupParam(name, label)

                elif _type == NatronEngine.Int2DParam:
                    param = new_node.createInt2DParam(name, label)

                elif _type == NatronEngine.Int3DParam:
                    param = new_node.createInt3DParam(name, label)

                elif _type == NatronEngine.IntParam:
                    param = new_node.createIntParam(name, label)

                elif _type == NatronEngine.OutputFileParam:
                    param = new_node.createOutputFileParam(name, label)

                elif _type == NatronEngine.PageParam:
                    param = new_node.createPageParam(name, label)

                elif _type == NatronEngine.ParametricParam:
                    nbCurves = 0
                    param = new_node.createParametricParam(name, label, nbCurves)

                elif _type == NatronEngine.PathParam:
                    param = new_node.createPathParam(name, label)

                elif _type == NatronEngine.StringParam:
                    param = new_node.createStringParam(name, label)
                    # si no tiene label, lo mas probable que sea una "eStringTypeLabel"
                    if not param.getLabel():
                        param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)

                if param:
                    if hasattr(p, 'getMinimum'):
                        param.setMinimum(p.getMinimum())
                        param.setMaximum(p.getMaximum())

            if param:
                param.setAddNewLine(p.getAddNewLine())
                param.copy(p)

        # crea una lista con los nodos hijos, para despues
        # conectarlos, cuando ya esten todos creados
        created_nodes = {}
        for child in node.getChildren():
            _node = copy(child, new_node)
            created_nodes[child.getScriptName()] = _node

        for child in node.getChildren():
            # datos del nodo de origen
            name = child.getScriptName()
            label = child.getLabel()
            position = child.getPosition()
            size = child.getSize()
            # ---------------

            _node = created_nodes[name]
            _node.setPosition(position[0], position[1])
            _node.setSize(size[0], size[1])
            _node.setLabel(label)

            for i in range(child.getMaxInputCount()):
                inode = child.getInput(i)
                if inode:
                    iname = inode.getScriptName()
                    _node.connectInput(i, created_nodes[iname])
    else:
        new_node = _app.createNode(_id, -1, group)
        new_node.setScriptName(node.getScriptName())
        disable_node = None

        for p in node.getParams():
            name = p.getScriptName()
            param = new_node.getParam(name)
            if param:
                # cuando se copia el parametro de 'OutputFile', Natron se pega cuando trata de recargar
                # el archivo, asi que para evitarlo, se desabilita el nodo,
                # y cuando ya copia todos los parametros, deja el nodo como estaba.
                if p.getTypeName() == 'OutputFile':
                    disable_node_param = new_node.getParam('disableNode')
                    disable_node = disable_node_param.get()
                    disable_node_param.set(True)
                # ------------------------------

                param.copy(p)

        if not disable_node == None:
            disable_node_param.set(disable_node)

    new_node.refreshUserParamsGUI()

    return new_node


def get_project_name():
    return app().getProjectParam('projectName').get()[:-4]


def get_project_path():
    return app().getProjectParam('projectPath').get() + app().getProjectParam('projectName').get()


def saveProject():
    project_path = get_project_path()
    app().saveProject(project_path)

    return project_path


def run(node, func_name, args=[]):
    # 'run' llama a una funcion que pertenece
    # al nodo, el modulo esta en el parametro 'onParamChanged'

    onParamChanged = node.getParam('onParamChanged')
    func = False
    if onParamChanged:
        core_module = onParamChanged.get().split('.')[0]
        try:
            exec('from ' + core_module + ' import ' + func_name)
            func = eval(func_name)
        except:
            None

    if func:
        func(*args)


def absolute(path):
    base_project = app().getProjectParam('projectPath').get()

    return path.replace('[Project]/', base_project)


def switch(thisNode, checkbox, input, output1, output2):
    _input = getNode(thisNode, input)

    _input.disconnectInput(0)
    if checkbox:
        _input.connectInput(0, getNode(thisNode, output2))
    else:
        _input.connectInput(0, getNode(thisNode, output1))


def get_node_by_label(label=None, group=None):
    if not group:
        group = app()

    # Encuentra un nodo a partir del Label
    for child in group.getChildren():
        if child.getLabel() == label:
            return child

    return None


def getNode(group=None, label=None):
    if not group:
        group = app()

    # cuando creamos nodos con un nombre de script que ya se uso alguna vez,
    # natron le pone otro nombre de script, por eso a veces no encontraremos el nodo
    # con el nombre de script, y si no lo encuentra lo busca por el 'label'; buscarlo con el 'label'
    # es mucho mas pesado por que tiene que iterar todo el grupo para encontrarlo, en cambio el scriptName
    # lo encuentra directamente por eso va primero.
    node = group.getNode(label)
    if node:
        return node
    # -----------------------------

    return get_node_by_label(label, group)


def get_nodes_by_type(workarea, type_name):
    nodes = []
    for node in workarea.getChildren():
        if node.getPluginID() == type_name:
            nodes.append(node)

    return nodes


def set_hash_script_name(node, label):
    node.setScriptName(label + str(hash_generator(5)))
    node.setLabel(label)


def createNode(node, label=None, group=None, position=None, color=None, output=None, force=True, script_hash=None):

    def set_name(n, name):
        if script_hash:
            set_hash_script_name(n, name)
        else:
            n.setScriptName(name)
            n.setLabel(name)

    if not force:
        # si el nodo existe, retorta ese nodo
        _node = getNode(group, label)
        if _node:
            set_name(_node, label)
            return _node

    nodes = {
        'blur': 'net.sf.cimg.CImgBlur',
        'text': 'net.fxarena.openfx.Text',
        'transform': 'net.sf.openfx.TransformPlugin',
        'merge': 'net.sf.openfx.MergePlugin',
        'output': 'fr.inria.built-in.Output',
        'position': 'net.sf.openfx.Position',
        'crop': 'net.sf.openfx.CropPlugin',
        'constant': 'net.sf.openfx.ConstantPlugin',
        'backdrop': 'fr.inria.built-in.BackDrop',
        'dot': 'fr.inria.built-in.Dot',
        'dissolve': 'net.sf.openfx.DissolvePlugin',
        'vinarender': 'vv.vinarender',
        'input': 'fr.inria.built-in.Input',
        'reformat': 'net.sf.openfx.Reformat',
        'rectangle': 'net.sf.openfx.Rectangle',
        'switch': 'net.sf.openfx.switchPlugin',
        'ntprender': 'vv.NtpRender',
        'videovina': 'vv.VideoVina',
        'slide_base': 'vv.SlideBase',
        'zoom_transition': 'vv.ZoomTransition',
        'statistics': 'net.sf.openfx.ImageStatistics',
        'keyer': 'net.sf.openfx.KeyerPlugin',
        'time_offset': 'net.sf.openfx.timeOffset'
    }

    if node in nodes.keys():
        _id = nodes[node]
    else:
        _id = node

    _node = app().createNode(_id, -1, group)
    if label:
        set_name(_node, label)

    if position:
        _node.setPosition(position[0], position[1])
    if color:
        _node.setColor(color[0], color[1], color[2])
    if output:
        output[1].connectInput(output[0], _node)

    return _node


def alert(message, title='Alert'):
    if not gui:
        return

    if _disable_dialog:
        return

    NatronGui.natron.informationDialog(title, str(message))


def warning(title, message):
    if not gui:
        return

    if _disable_dialog:
        return

    NatronGui.natron.warningDialog(title, message)


def question(_question, message):
    if not gui:
        return True

    if _disable_dialog:
        return True

    msgBox = QMessageBox()
    msgBox.setText(message)
    msgBox.setInformativeText(_question)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Ok)
    ret = msgBox.exec_()

    if ret == QMessageBox.Ok:
        return True
    else:
        return False


def get_all_nodes(group=None):
    if not group:
        group = app()
    nodes = []
    for a in group.getChildren():
        nodes.append(a)
        for b in a.getChildren():
            nodes.append(b)
            for c in b.getChildren():
                nodes.append(c)
                for d in c.getChildren():
                    nodes.append(d)
                    for e in d.getChildren():
                        nodes.append(e)
    return nodes


def get_all_path_nodes(group=None):
    if not group:
        group = app()
    nodes = []
    for a in group.getChildren():
        a_path = a.getScriptName()
        nodes.append([a, a_path])
        for b in a.getChildren():
            b_path = a.getScriptName() + '.' + b.getScriptName()
            nodes.append([b, b_path])
            for c in b.getChildren():
                c_path = a.getScriptName() + '.' + b.getScriptName() + '.' + c.getScriptName()
                nodes.append([c, c_path])
                for d in c.getChildren():
                    d_path = a.getScriptName() + '.' + b.getScriptName() + '.' + \
                        c.getScriptName() + '.' + d.getScriptName()
                    nodes.append([d, d_path])
                    for e in d.getChildren():
                        e_path = a.getScriptName() + '.' + b.getScriptName() + '.' + c.getScriptName() + \
                            '.' + d.getScriptName() + '.' + e.getScriptName()
                        nodes.append([e, e_path])
    return nodes


def get_select_node(_type=None):
    for node in app().getSelectedNodes():
        if _type:
            if node.getPluginID() == _type:
                return node
        else:
            return node

    return None


def get_connected_nodes(parent, parent_include=True):
    if not parent:
        return []

    # obtiene todos los nodos conectados a un nodo padre
    nodes = []

    def add(parent):
        inputs = parent.getMaxInputCount()

        for i in range(inputs):
            node = parent.getInput(i)
            if node:
                # verifica si el nodo que se va a sumar, no tiene el mismo nombre que alguno que este en la lista
                name = node.getScriptName()
                is_in_list = any(node.getScriptName() ==
                                 name for node in nodes)
                if not is_in_list:
                    nodes.append(node)
                    add(node)

    if parent_include:
        nodes.append(parent)
    add(parent)

    return nodes


def node_delete(nodes):
    # se usa .destroy() 2 veces ya que a veces
    # natron no borra el nodo
    if type(nodes) is list:
        for n in nodes:
            if n:
                n.setPosition(10000, 10000)
                n.destroy()
        for n in nodes:
            if n:
                n.destroy()
    else:
        # mueve el nodo a otro lado, por que a veces queda el nodo en el node graph
        nodes.setPosition(10000, 10000)

        nodes.destroy()
        nodes.destroy()


def dots_delete(parent_node):
    # borra todos los dot de un grupo para aligerar el proyecto

    def find_input(node, i):
        # encuentra el nodo origen, omitiendo los 'dot'
        input_node = node.getInput(i)
        if input_node:
            if input_node.getPluginID() == 'fr.inria.built-in.Dot':
                return find_input(input_node, 0)
            else:
                return input_node
        else:
            return None

    dots = []
    for node in parent_node.getChildren():
        if node.getPluginID() == 'fr.inria.built-in.Dot':
            dots.append(node)
        else:
            for i in range(node.getMaxInputCount()):
                input_node = find_input(node, i)
                if input_node:
                    node.disconnectInput(i)
                    node.connectInput(i, input_node)

    node_delete(dots)


def get_node_path(node):
    # encuentra la ruta completa del nodo, si es que
    # el nodo a buscar esta dentro de un grupo.
    node_name = node.getScriptName()
    node_position = node.getPosition()[0]

    found = None
    for a in app().getChildren():
        a_name = a.getScriptName()
        a_pos = a.getPosition()[0]
        if a_name == node_name:
            if a_pos == node_position:
                found = ''
                break

        for b in a.getChildren():
            b_name = b.getScriptName()
            b_pos = b.getPosition()[0]
            if b_name == node_name:
                if b_pos == node_position:
                    found = a_name
                    break

            for c in b.getChildren():
                c_name = c.getScriptName()
                c_pos = c.getPosition()[0]
                if c_name == node_name:
                    if c_pos == node_position:
                        found = a_name + '.' + b_name
                        break
    return found


def get_parent(node):
    # obtiene el nodo padre
    _app = app()
    node_path = get_node_path(node)

    if node_path:
        return eval('_app.getNode("' + node_path + '")')
    else:
        return _app


def get_output_nodes(node):
    nodes = []
    for n, path in get_all_path_nodes():
        for i in range(n.getMaxInputCount()):
            input_node = n.getInput(i)
            if input_node:
                if input_node.getScriptName() == node.getScriptName():
                    nodes.append([n, i])

    return nodes


def input_connected(node, _input=0):
    # si el bounding box es 0, significa que no hay imagen conectada
    input_node = node.getInput(_input)
    if input_node:
        if input_node.getRegionOfDefinition(0, 0).x2:
            return True

    return False


def get_output(group):
    # obtiene el nodo 'Output' de un grupo, si no esta,
    # lo busca por alguna interacion; 'Output1', 'Output2', etc.
    output = group.getNode('Output')

    if output:
        return output

    for i in range(10):
        output_name = 'Output' + str(i)
        output = group.getNode(output_name)

        if output:
            return output

    return None


def get_bbox(node, frame=1):
    # obtiene el bounding box de la imagen.
    # Natron no muestra el bbox cuando es un grupo, por eso si
    # es un grupo busca el bbox en el nodo 'Output'.
    bbox = node.getRegionOfDefinition(frame, 1)

    x1 = bbox.x1
    x2 = bbox.x2
    y1 = bbox.y1
    y2 = bbox.y2

    if not (x1 + x2 + y1 + y2):
        output = get_output(node)
        if output:
            bbox = output.getRegionOfDefinition(frame, 1)

            x1 = bbox.x1
            x2 = bbox.x2
            y1 = bbox.y1
            y2 = bbox.y2

    return Namespace(
        x1=x1,
        x2=x2,
        y1=y1,
        y2=y2
    )


def get_bbox_format(node):

    bbox = get_bbox(node)
    width = int(bbox.x2 - bbox.x1)
    height = int(bbox.y2 - bbox.y1)

    return [width, height]


def bbox_bake(crop, start_frame, last_frame):
    input_node = crop.getInput(0)
    if not input_node:
        return

    bottom_left = crop.getParam('bottomLeft')
    size = crop.getParam('size')

    bottom_left.restoreDefaultValue(0)
    bottom_left.restoreDefaultValue(1)

    size.restoreDefaultValue(0)
    size.restoreDefaultValue(1)

    for frame in range(start_frame, last_frame):
        bbox = get_bbox(input_node, frame)

        bottom_left.setValueAtTime(bbox.x1, frame, 0)
        bottom_left.setValueAtTime(bbox.y1, frame, 1)
        size.setValueAtTime(bbox.x2 - bbox.x1, frame, 0)
        size.setValueAtTime(bbox.y2 - bbox.y1, frame, 1)


def set_option(param, option):
    try:
        index = param.getOptions().index(option)
        param.set(index)
    except:
        None


def autocrop(workarea, image_node, crop_node, each_pixel=10):
    bbox = get_bbox(image_node)

    image_statictis = getNode(workarea, 'autocrop')
    if not image_statictis:
        image_statictis = createNode('statistics', 'autocrop', workarea)

    image_statictis.disconnectInput(0)
    image_statictis.connectInput(0, image_node)

    clear = image_statictis.getParam('clearSequence')
    max_param = image_statictis.getParam('statMax')

    width = int(bbox.x2 - bbox.x1)
    height = int(bbox.y2 - bbox.y1)

    def left_adjust(each_pixel, left):
        max_param.setValue(0, 0)
        clear.trigger()
        for i in range(width):
            image_statictis.getParam('bottomLeft').set(left, bbox.y1)
            image_statictis.getParam('size').set(each_pixel, height)
            image_statictis.getParam('analyzeFrame').trigger()

            if max_param.get()[0] > 0:
                break
            else:
                left += each_pixel

        return left

    def bottom_adjust(each_pixel, bottom):
        max_param.setValue(0, 0)
        clear.trigger()
        for i in range(height):
            image_statictis.getParam('bottomLeft').set(bbox.x1, bottom)
            image_statictis.getParam('size').set(width, each_pixel)
            image_statictis.getParam('analyzeFrame').trigger()

            if max_param.get()[0] > 0:
                break
            else:
                bottom += each_pixel

        return bottom

    def right_adjust(each_pixel, right):
        max_param.setValue(0, 0)
        clear.trigger()
        for i in range(width):
            if max_param.get()[0] > 0:
                break
            else:
                right -= each_pixel

            image_statictis.getParam('bottomLeft').set(right, bbox.y1)
            image_statictis.getParam('size').set(each_pixel, height)
            image_statictis.getParam('analyzeFrame').trigger()

        return right

    def top_adjust(each_pixel, top):
        max_param.setValue(0, 0)
        clear.trigger()
        for i in range(height):
            if max_param.get()[0] > 0:
                break
            else:
                top -= each_pixel

            image_statictis.getParam('bottomLeft').set(bbox.x1, top)
            image_statictis.getParam('size').set(width, each_pixel)
            image_statictis.getParam('analyzeFrame').trigger()

        return top

    #

    left = left_adjust(each_pixel, bbox.x1)
    bottom = bottom_adjust(each_pixel, bbox.y1)
    right = right_adjust(each_pixel, bbox.x1 + width)
    top = top_adjust(each_pixel, bbox.y1 + height)

    #

    _width = right - left + each_pixel
    _height = top - bottom + each_pixel

    crop_node.getParam('bottomLeft').set(left, bottom)
    crop_node.getParam('size').set(_width, _height)


def restore_default(param):
    if hasattr(param, 'restoreDefaultValue'):
        dimensions = param.getNumDimensions()
        if dimensions > 1:
            for dimension in range(dimensions):
                param.restoreDefaultValue(dimension)
        else:
            param.restoreDefaultValue()


def reload_read(read_node):
    filename_param = read_node.getParam('filename')
    filename = filename_param.get()

    before_param = read_node.getParam('before')
    after_param = read_node.getParam('after')
    if before_param and after_param:
        before = before_param.get()
        after = after_param.get()

    filename_param.reloadFile()
    filename_param.reloadFile()

    if before_param and after_param:
        before_param.set(before)
        after_param.set(after)


def reload_all_read(node):
    # recarga todos los archivos 'read' del grupo
    for n in node.getChildren():
        if n.getPluginID() == 'fr.inria.built-in.Read':
            reload_read(n)


def change_read_filename(read_node, value):

    filename = read_node.getParam('filename')

    # si la ruta es igual a la existete retorna para no gastar recursos
    if filename.get() == value:
        return

    # obtiene parametros actuales antes de cambiar la ruta, por que si se
    # cambia el 'filename' todos estos parametros quedan por defecto.
    before_param = read_node.getParam('before')
    after_param = read_node.getParam('after')
    if before_param and after_param:
        before = before_param.get()
        after = after_param.get()

    first_frame_param = read_node.getParam('firstFrame')
    last_frame_param = read_node.getParam('lastFrame')
    if first_frame_param and last_frame_param:
        first_frame = first_frame_param.get()
        last_frame = last_frame_param.get()

    # cambia ruta
    filename.set(value)

    # deja estos parametros con los valores anteriores
    if before_param and after_param:
        before_param.set(before)
        after_param.set(after)

    if first_frame_param and last_frame_param:
        first_frame_param.set(first_frame)
        last_frame_param.set(last_frame)


def get_current_choice(choice_param):
    index = choice_param.getValue()
    option = choice_param.getOption(index)

    return option.split('- ')[-1].replace(' ', '_').lower()


def set_choice_list(choice_param, list):
    items = []
    for i, item_name in enumerate(sorted(list)):
        name = str(i + 1) + ' - ' + item_name.replace('_', ' ').capitalize()
        items.append((name, item_name))

    choice_param.setOptions(items)
