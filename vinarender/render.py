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
fps = data['fps']

ext = output.split('.')[-1]

app.loadProject(project)

node = eval('app.getNode("' + node + '")')
if not node:
    node = get_videovina_render()

writer = app.createWriter(output)

# el tamanio del render es igual al del nodo
writer.getParam('formatType').setValue(0)
# ---------------------
writer.getParam("fps").set(fps)

# codecs name
# prores_ksap4h - Apple ProRess 4444
# prores_ksapch - Apple ProRess 422 HQ
# prores_ksapcn - Apple ProRess 422
# libx264 - H264
# --------------------
if video_format == 0:  # mov
    codec = 'prores_ksapcn'
    format = 'mov'
elif video_format == 1:  # mp4
    codec = 'libx264'
    format = 'mp4'
    crf = writer.getParam('crf')
    crf.set(output_quality + 3)

# parametros de codec solo si no es una secuencia de imagenes
if video_format < 2:
    format_param = writer.getParam('format')
    format_index = format_param.getOptions().index(format)
    format_param.set(format_index)

    codec_param = writer.getParam('codec')
    codec_index = codec_param.getOptions().index(codec)
    codec_param.set(codec_index)

writer.connectInput(0, node)
