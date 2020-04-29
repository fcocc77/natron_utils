import os

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()
    if knob_name == 'render':
        render(thisNode, app)

def get_node_path(thisNode, app):
    # encuentra la ruta completa del nodo, si es que
    # el nodo a buscar esta dentro de un grupo.

    vian_name = thisNode.getScriptName()
    app_name = 'app1'
    found = None
    for a in app.getChildren():
        a_name = a.getScriptName()
        
        if a_name == vian_name:
            found = app_name + '.'
            break

        for b in a.getChildren():
            b_name = b.getScriptName()
            if b_name == vian_name:
                found = app_name + '.' + a_name + '.'
                break

            for c in b.getChildren():
                c_name = c.getScriptName()
                if c_name == vian_name:
                    found = app_name + '.' + a_name + '.' + b_name + '.'
                    break

    return found
         
def render(thisNode, app):
    filename = thisNode.filename.get()
    x = thisNode.resolution.boxSize.getValue(0)
    y = thisNode.resolution.boxSize.getValue(1)

    first_frame = thisNode.frame_range.frameRange.getValue(0)
    last_frame = thisNode.frame_range.frameRange.getValue(1)

    submit = '/opt/vinarender/bin/submit'

    job_name = 'natron_render'
    server_group = 'Natron'
    task_size = thisNode.task_size.get()
    project = app.projectPath.get() + app.projectName.get()
    software = 'Natron'
    render = get_node_path(thisNode, app) + thisNode.getInput(0).getScriptName()

    cmd = ( submit 
        + ' -jobName ' + job_name
        + ' -serverGroup ' + server_group
        + ' -firstFrame ' + str( first_frame )
        + ' -lastFrame ' + str( last_frame )
        + ' -taskSize ' + str( task_size )
        + ' -project "' + project + '"'
        + ' -software ' + software
        + ' -render ' + render
    )

    
    print cmd

    # os.system( cmd )