import os
from nx import get_parent

# videovina modules
from slides import *
from api import *
from song import *
from develop import *
from vv_misc import *
from production import *
from pictures import *


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    workarea = get_parent(thisNode)

    knob_name = thisParam.getScriptName()

    project_path = os.path.dirname(os.path.dirname(app.projectPath.get()))

    if knob_name == 'generate_slides':
        generate_base_slides(thisNode, app, workarea)

    elif knob_name == 'prerender':
        divide_project(thisNode, workarea)

    elif knob_name == 'refresh':
        refresh()

    elif knob_name == 'generate_production_slides':
        production_slides(thisNode, app, workarea)

    elif knob_name == 'videovina_info':
        export_videovina_info(thisNode, app, workarea, project_path)

    elif knob_name == 'update_videovina_project':
        update_videovina_project(thisNode, app, workarea)

    elif knob_name == 'default_color':
        set_default_color(thisNode, thisParam)

    elif knob_name == 'include_texts':
        color_if_has_text(thisNode, thisParam)

    elif knob_name == 'videovina_root':
        update_private_content(thisNode, thisParam)

    elif knob_name == 'play':
        play_song(thisNode)

    elif knob_name == 'stop':
        play_song(thisNode, play=False)

    elif knob_name == 'transfer_to_static':
        transfer_to_static(thisNode, app, project_path)

    elif knob_name == 'clean':
        clean(thisNode, workarea)

    elif knob_name == 'generate_pictures':
        generate_random_pictures(thisNode, app, workarea)
        update_post_fx()
        refresh()

    elif knob_name == 'last_slide_delete':
        clamp_slides(0, thisNode.getParam('last_slide').get())
        update_post_fx()
