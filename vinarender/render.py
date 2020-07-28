from sys import argv
import NatronEngine
from vina import get_videovina_render
import json

app = app1

data = json.loads(argv[6].replace("'", '"'))

project = argv[5] + '.ntp'
node = data['render_node']
output = data['output']
video_format = data['video_format']
output_quality = data['output_quality']

ext = output.split('.')[-1]

app.loadProject(project)

node = eval('app.getNode("' + node + '")')
if not node:
    node = get_videovina_render()

writer = app.createWriter(output)

# el tamanio del render es igual al del nodo
writer.getParam('formatType').setValue(0)
# ---------------------

# 0 = ap4h Apple ProRess 4444
# 1 = apch Apple ProRess 422 HQ
# 2 = apcn Apple ProRess 422
if ext == 'mov':
    writer.getParam('codec').setValue(2)
    writer.getParam("fps").set(30)
# ------------------

writer.connectInput(0, node)
