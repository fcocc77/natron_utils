from sys import argv
import NatronEngine
from vina import get_videovina_render

app = app1

project = argv[5] + '.ntp'
node = argv[6]
output = argv[7]
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
