from util import *
import NatronGui
import NatronEngine
from PySide.QtGui import QMessageBox

def copy(node, group):
	app = NatronGui.natron.getGuiInstance(0)

	_id = node.getPluginID()
	new_node = app.createNode(_id, 0, group)

	for p in node.getParams():	
		name = p.getScriptName()			
		param = new_node.getParam(name)
		param.copy(p)

	return new_node

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

def getNode(group, label = None):
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
		'dissolve': 'net.sf.openfx.DissolvePlugin'
	}

	_node = app.createNode(nodes[node], 2, group)
	_node.setLabel(label)
	if position:
		_node.setPosition(position[0], position[1])
	if color:
		_node.setColor(color[0], color[1], color[2])
	if output:
		output[1].connectInput(output[0], _node)

	return _node

def alert(message):
	NatronGui.natron.informationDialog('Alert', str(message))

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
					d_path = a.getScriptName() + '.' + b.getScriptName() + '.' + c.getScriptName() + '.' + d.getScriptName()
					nodes.append([d, d_path])
					for e in d.getChildren(): 
						e_path = a.getScriptName() + '.' + b.getScriptName() + '.' + c.getScriptName() + '.' + d.getScriptName() + '.' + e.getScriptName()
						nodes.append([e, e_path])
	return nodes