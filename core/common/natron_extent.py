from util import *
import NatronEngine
from PySide.QtGui import QMessageBox
try:
    import NatronGui
except:
    None


def app():
    return NatronEngine.natron.getActiveInstance()


def copy(node, group=None):
    _app = app()
    _id = node.getPluginID()

    # si el nodo es un grupo, busca cada parametro en el nodo de origen
    # y lo crea en el nuevo nodo grupo, y luega copia cada nodo hijo con sus atributos
    if _id == 'fr.inria.built-in.Group':
        new_node = _app.createNode('vv.group', 1, group)

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
                    param = new_node.createParametricParam(
                        name, label, nbCurves)

                elif _type == NatronEngine.PathParam:
                    param = new_node.createPathParam(name, label)

                elif _type == NatronEngine.StringParam:
                    param = new_node.createStringParam(name, label)
                    # si no tiene label, lo mas probable que sea una "eStringTypeLabel"
                    if not param.getLabel():
                        param.setType(
                            NatronEngine.StringParam.TypeEnum.eStringTypeLabel)

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
        for p in node.getParams():
            name = p.getScriptName()
            param = new_node.getParam(name)
            if param:
                param.copy(p)

    new_node.setScriptName(node.getScriptName())
    new_node.refreshUserParamsGUI()

    return new_node


def get_project_name():
    return app().getProjectParam('projectName').get()[:-4]


def saveProject():
    project_path = app().getProjectParam('projectPath').get() + app().getProjectParam('projectName').get()
    app().saveProject(project_path)

    return project_path


def run(node, func_name, args=[]):
    # esta funcion llama a una funcion del plugin

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


def question(_question, message):
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


def getNode(group=None, label=None):
    if not group:
        group = app()

    # Encuentra un nodo a partir del Label
    for child in group.getChildren():
        if child.getLabel() == label:
            return child

    return None


def createNode(node=None, label=None, group=None, position=None, color=None, output=None):
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
        'switch': 'net.sf.openfx.switchPlugin'
    }

    _node = app().createNode(nodes[node], -1, group)
    _node.setLabel(label)
    if position:
        _node.setPosition(position[0], position[1])
    if color:
        _node.setColor(color[0], color[1], color[2])
    if output:
        output[1].connectInput(output[0], _node)

    return _node


def alert(message, title='Alert'):
    NatronGui.natron.informationDialog(title, str(message))


def warning(title, message):
    NatronGui.natron.warningDialog(title, message)


def value_by_durations(value, durations=[0, 0, 0]):
    normal_speed = durations[1]

    slow = (value * durations[0]) / normal_speed
    fast = (value * durations[2]) / normal_speed

    return [slow, value, fast]


def get_all_nodes(group=None):
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


def get_connected_nodes(parent):
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

    nodes.append(parent)
    add(parent)

    return nodes


def delete(nodes):
    # se usa .destroy() 2 veces ya que a veces
    # natron no borra el nodo
    if type(nodes) is list:
        for n in nodes:
            n.setPosition(10000, 10000)
            n.destroy()
        for n in nodes:
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

    delete(dots)


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
    for n, path in get_all_nodes():
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
