import os
import shutil
from util import jread
from natron_extent import get_connected_nodes, saveProject, absolute, warning, alert, get_node_path


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode, app)
    if knob_name == 'range' or knob_name == 'readfile':
        change_paramaters(thisNode)
    if knob_name == 'project_frame_range':
        frame_range = app.frameRange.get()
        thisNode.range.set(frame_range[0], frame_range[1])


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


def check_project(thisNode):
    path_list = jread('/opt/vinarender/etc/preferences_s.json').paths.system
    paths = []
    for r in path_list:
        if os.path.isdir(r):
            paths.append(r)
    if not paths:
        paths.append("#none#")

    local_filename = ''
    disconnect_filename = ''

    ok = True

    for node in get_connected_nodes(thisNode):
        filename_param = node.getParam("filename")
        if filename_param:
            filename = filename_param.get()

            dirname = os.path.dirname(filename)
            relative = '[Project]'

            if relative in filename:
                None
            elif not os.path.isdir(dirname):
                disconnect_filename += node.getLabel() + ' = ' + filename + '\n'
                ok = False
            else:
                is_in_vinarender_paths = False
                for p in paths:
                    if p in filename:
                        is_in_vinarender_paths = True
                if not is_in_vinarender_paths:
                    ok = False
                    local_filename += node.getLabel() + ' = ' + filename + '\n'

    if ok:
        return True
    else:
        line1 = ''
        line2 = ''
        if local_filename:
            line1 = "These files are on your PC:"
        if disconnect_filename:
            line2 = "These files are disconnected:"

        message = line1 + '\n\n' + local_filename + \
            '\n\n' + line2 + '\n\n' + disconnect_filename
        warning('FileName Error', message)
        return False


def render(thisNode, app):
    node_input = thisNode.getInput(0)
    if not node_input:
        warning('VinaRender', '!You must connect the image.')
        return

    if not check_project(thisNode):
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

    node_path = get_node_path(thisNode)
    if node_path:
        node_path += '.'
    render = node_path + thisNode.getScriptName() + '.' + output_node

    output = absolute(thisNode.filename.getValue())
    instances = thisNode.instances.getValue()
    project = saveProject()

    if thisNode.getParam('duplicate_project').get():
        # guarda el proyecto antes de enviar, y crea uno nuevo
        for i in range(1000):
            # encuentra version disponible
            dirname = os.path.dirname(project)
            basename = os.path.basename(project)
            new_project = dirname + '/__' + \
                basename[:-4] + '_render_' + str(i + 1) + '.ntp'
            if not os.path.isfile(new_project):
                break
        shutil.copy(project, new_project)
        project = new_project

    cmd = (submit
           + ' -jobName "' + job_name + '"'
           + ' -serverGroup ' + server_group
           + ' -firstFrame ' + str(first_frame)
           + ' -lastFrame ' + str(last_frame)
           + ' -taskSize ' + str(task_size)
           + ' -project "' + project + '"'
           + ' -software ' + software
           + ' -render ' + render
           + ' -extra ' + output
           + ' -instances ' + str(instances)
           )

    os.system(cmd)

    if (not thisNode.no_dialog.get()):
        alert('Render Sended.', 'VinaRender')
