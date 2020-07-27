# api: este archivo permite subministrar un proyecto videovina,
# que se envio desde el editor web de videovina.
from nx import createNode

videovina_project = '/home/pancho/Documents/GitHub/videovina/tmp/as3/private/admin/projects/testing/project.json'
base_projects_dir = "/home/pancho/Documents/GitHub/videovina/private/templates_base/testing/comp/ntp"
multi_project_dir = "/home/pancho/Documents/GitHub/videovina/private/templates_base/testing/comp/casa"
user = 'admin'
project_name = 'testing'

# creacion de nodo videovina y ntprender
vinarender_node = createNode('videovina')
ntprender = createNode('ntprender')
ntprender.connectInput(0, vinarender_node)

# actualiza los datos del proyecto de videovina al nodo videovina
vinarender_node.getParam('videovina_project').set(videovina_project)
vinarender_node.getParam('update_videovina_project').trigger()

# envia a crear los proyectos a vinarender
ntprender.getParam('output_folder').set(base_projects_dir)
ntprender.getParam('output_production_folder').set(multi_project_dir)
ntprender.getParam('job_name').set('multi_project: ' + user + ':' + project_name)
ntprender.getParam('send_as_production').trigger()
