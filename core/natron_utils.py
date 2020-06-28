from util import *
import NatronGui
import NatronEngine
from PySide.QtGui import QMessageBox


def copy(node, group=None):
    app = NatronGui.natron.getGuiInstance(0)
    _id = node.getPluginID()

    # si el nodo es un grupo, busca cada parametro en el nodo de origen
    # y lo crea en el nuevo nodo grupo, y luega copia cada nodo hijo con sus atributos
    if _id == 'fr.inria.built-in.Group':
        new_node = app.createNode('vv.group', 1, group)

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
                    # usar esto si es un label:
                    # param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeLabel)

                if param:
                    if hasattr(p, 'getMinimum'):
                        param.setMinimum(p.getMinimum())
                        param.setMaximum(p.getMaximum())

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
            input_count = child.getMaxInputCount()
            position = child.getPosition()
            size = child.getSize()
            # ---------------

            _node = created_nodes[name]
            _node.setPosition(position[0], position[1])
            _node.setSize(size[0], size[1])
            _node.setLabel(label)

            for i in range(input_count):
                inode = child.getInput(i)
                if inode:
                    iname = inode.getScriptName()
                    _node.connectInput(i, created_nodes[iname])
    else:
        new_node = app.createNode(_id, -1, group)
        for p in node.getParams():
            name = p.getScriptName()
            param = new_node.getParam(name)
            param.copy(p)

    new_node.setScriptName(node.getScriptName())
    new_node.refreshUserParamsGUI()

    return new_node


def saveProject():
    app = NatronGui.natron.getGuiInstance(0)

    project_path = app.getProjectParam('projectPath').get(
    ) + app.getProjectParam('projectName').get()
    app.saveProject(project_path)

    return project_path


def absolute(path):
    app = NatronGui.natron.getGuiInstance(0)
    base_project = app.getProjectParam('projectPath').get()

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


def getNode(group, label=None):
    # Encuentra un nodo a partir del Label
    for child in group.getChildren():
        if child.getLabel() == label:
            return child

    return None


def createNode(node=None, label=None, group=None, position=None, color=None, output=None):
    app = NatronGui.natron.getGuiInstance(0)
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

    _node = app.createNode(nodes[node], -1, group)
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


def value_by_speed(value, speeds=[0, 0, 0]):
    normal_speed = speeds[1]

    slow = (value * speeds[0]) / normal_speed
    fast = (value * speeds[2]) / normal_speed

    return [slow, value, fast]


def get_all_nodes(app):
    nodes = []
    for a in app.getChildren():
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
