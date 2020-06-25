import os
import shutil
import NatronGui
from util import jread
from natron_utils import get_all_nodes, saveProject, absolute

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode, app)
    if knob_name == 'range' or knob_name =='readfile':
        change_paramaters(thisNode)
    if knob_name == 'project_frame_range':
        frame_range = app.frameRange.get()
        thisNode.range.set( frame_range[0], frame_range[1] )

def change_paramaters(thisNode):
    frame_range = thisNode.getNode('frame_range')
    if not frame_range:
        return
    first_frame = frame_range.getParam('frameRange').getValue(0)
    last_frame = frame_range.getParam('frameRange').getValue(1)

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
        output_node = 'Source'

    filename = thisNode.filename.get()

    first_frame = thisNode.frame_range.frameRange.getValue(0)
    last_frame = thisNode.frame_range.frameRange.getValue(1)

    submit = '/opt/vinarender/bin/submit'

    project_name = app.projectName.get()

    job_name = thisNode.job_name.get()
    if not job_name:
        job_name = project_name.split('.')[0]
    server_group = 'Natron'
    task_size = thisNode.task_size.get()
    software = 'Natron'
    render = get_node_path(thisNode, app) + thisNode.getScriptName() + '.' + output_node
    output = absolute(thisNode.filename.getValue())
    instances = thisNode.instances.getValue()

    # guarda el proyecto antes de enviar, y crea uno nuevo
    project_path = saveProject()
    for i in range(100):
        # encuentra version disponible
        dirname = os.path.dirname(project_path)
        basename = os.path.basename(project_path) 
        new_project = dirname + '/__' + basename[:-4] + '_render_' + str(i + 1) + '.ntp'
        if not os.path.isfile( new_project ):
            break
    shutil.copy(project_path, new_project)    
    # ------------------

    cmd = ( submit 
        + ' -jobName "' + job_name +'"'
        + ' -serverGroup ' + server_group
        + ' -firstFrame ' + str( first_frame )
        + ' -lastFrame ' + str( last_frame )
        + ' -taskSize ' + str( task_size )
        + ' -project "' + new_project + '"'
        + ' -software ' + software
        + ' -render ' + render
        + ' -extra ' + output
        + ' -instances ' + str( instances )
    )

    os.system( cmd )

    if (not thisNode.no_dialog.get()):
        NatronGui.natron.informationDialog('VinaRender', 'Render Sended.')