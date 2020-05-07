import os
import NatronGui
from util import jread
from natron import get_all_nodes


def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode, app)
    if knob_name == 'range' or knob_name =='readfile':
        change_paramaters(thisNode)

def change_paramaters(thisNode):
    first_frame = thisNode.frame_range.frameRange.getValue(0)
    last_frame = thisNode.frame_range.frameRange.getValue(1)

    thisNode.reading.firstFrame.setValue(first_frame)
    thisNode.reading.lastFrame.setValue(last_frame)

    thisNode.reading.before.setValue(3)
    thisNode.reading.after.setValue(3)

    # cambia el premult de salida para que los .png no queden
    # con el borde negro.
    thisNode.reading.outputPremult.setValue(0)

def check_project(app):

    path_list = jread( '/opt/vinarender/etc/preferences_s.json' ).paths.system
    paths = []
    for r in path_list:
        if os.path.isdir(r):
            paths.append(r)
    if not paths:
        paths.append("#none#")

    local_filename = ''
    disconnect_filename = ''

    ok = True

    for node, node_path in get_all_nodes(app):
        filename_param = node.getParam("filename")
        if filename_param:
            filename = filename_param.get()

            dirname = os.path.dirname(filename)
            relative = '[Project]'
            
            if relative in filename:
                None
            elif not os.path.isdir(dirname):
                disconnect_filename += node_path + ' = ' + filename + '\n'
                ok = False
            else:
                is_in_vinarender_paths = False
                for p in paths:
                    if p in filename:
                        is_in_vinarender_paths = True
                if not is_in_vinarender_paths:
                    ok = False
                    local_filename += node_path + ' = ' + filename + '\n'

    if ok:
        return True
    else:
        line1 = ''
        line2 = ''
        if local_filename:
            line1 = "These files are on your PC:"
        if disconnect_filename:
            line2 = "These files are disconnected:"

        message = line1 + '\n\n' + local_filename + '\n\n' + line2 + '\n\n' + disconnect_filename
        NatronGui.natron.warningDialog( 'FileName Error', message )
        return False

def get_node_path(thisNode, app):
    # encuentra la ruta completa del nodo, si es que
    # el nodo a buscar esta dentro de un grupo.

    vina_name = thisNode.getScriptName()
    vina_position = thisNode.getPosition()[0]

    found = None
    for a in app.getChildren():
        a_name = a.getScriptName()
        a_pos = a.getPosition()[0]
        if a_name == vina_name:
            if a_pos == vina_position:
                found = ''
                break

        for b in a.getChildren():
            b_name = b.getScriptName()
            b_pos = b.getPosition()[0]
            if b_name == vina_name:
                if b_pos == vina_position:
                    found = a_name + '.'
                    break

            for c in b.getChildren():
                c_name = c.getScriptName()
                c_pos = c.getPosition()[0]
                if c_name == vina_name:
                    if c_pos == vina_position:
                        found = a_name + '.' + b_name + '.'
                        break
    return found

def render(thisNode, app):
    node_input = thisNode.getInput(0)
    if not node_input:
        NatronGui.natron.warningDialog('VinaRender', '!You must connect the image.')
        return

    if not check_project(app):
        return
    
    rgb_only = thisNode.rgbonly.get()
    if rgb_only:
        output_node = 'to_rgb'
    else:
        output_node = 'Input1'

    filename = thisNode.filename.get()

    first_frame = thisNode.frame_range.frameRange.getValue(0)
    last_frame = thisNode.frame_range.frameRange.getValue(1)

    submit = '/opt/vinarender/bin/submit'

    project_name = app.projectName.get()

    job_name = project_name.split('.')[0]
    server_group = 'Natron'
    task_size = thisNode.task_size.get()
    project = app.projectPath.get() + project_name
    software = 'Natron'
    render = get_node_path(thisNode, app) + thisNode.getScriptName() + '.' + output_node
    output = thisNode.filename.getValue()
    output = output.replace( '[Project]/', app.projectPath.get() )
    instances = thisNode.instances.getValue()

    cmd = ( submit 
        + ' -jobName ' + job_name
        + ' -serverGroup ' + server_group
        + ' -firstFrame ' + str( first_frame )
        + ' -lastFrame ' + str( last_frame )
        + ' -taskSize ' + str( task_size )
        + ' -project "' + project + '"'
        + ' -software ' + software
        + ' -render ' + render
        + ' -extra ' + output
        + ' -instances ' + str( instances )
    )

    # guarda el proyecto antes de enviar el render
    project_path = app.projectPath.get() + app.projectName.get()
    app.saveProject( project_path )    
    # ------------------

    os.system( cmd )
    NatronGui.natron.informationDialog('VinaRender', 'Render Sended.')