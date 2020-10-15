from sys import argv
import NatronEngine
from vina import get_videovina_render
from nx import set_option, get_all_nodes, change_read_filename
import json

app = app1

data = json.loads(argv[6].replace("'", '"'))

project = argv[5] + '.ntp'
node = data['render_node']
output = data['output']
output_quality = data['output_quality']
fps = data['fps']
rgb_only = data['rgb_only']
src_path = data['src_path']
dst_path = data['dst_path']

ext = output.split('.')[-1]

app.loadProject(project)

node = eval('app.getNode("' + node + '")')
if not node:
    node = get_videovina_render()

writer = app.createWriter(output)
writer.connectInput(0, node)

# el tamanio del render es igual al del nodo
writer.getParam('formatType').setValue(0)

output_components = writer.getParam('outputComponents')
set_option(output_components, 'RGB')
writer.getParam('inputPremult').set(0)  # Opaque

if ext == 'png':
    if not rgb_only:
        set_option(output_components, 'RGBA')
        writer.getParam('inputPremult').set(2)  # unPremult

# codecs name
# prores_ksap4h - Apple ProRess 4444
# prores_ksapch - Apple ProRess 422 HQ
# prores_ksapcn - Apple ProRess 422
# libx264 - H264
if ext == 'mov':
    codec = 'prores_ksapcn'
    format = 'mov'
elif ext == 'mp4':
    codec = 'libx264'
    format = 'mp4'
    crf = writer.getParam('crf')
    crf.set(output_quality + 3)

# parametros de codec solo para los video mov y mp4
if ext == 'mov' or ext == 'mp4':
    fps_param = writer.getParam("fps")
    fps_param.set(fps)

    format_param = writer.getParam('format')
    format_index = format_param.getOptions().index(format)
    format_param.set(format_index)

    codec_param = writer.getParam('codec')
    codec_index = codec_param.getOptions().index(codec)
    codec_param.set(codec_index)
#
#


# Cambia todas las rutas del proyecto a las que corresponda al entorno.
for node in get_all_nodes():
    node_id = node.getPluginID()

    if node_id == 'fr.inria.built-in.Read':
        filename = node.getParam('filename')
        filename_value = filename.get().replace(src_path, dst_path)
        change_read_filename(node, filename_value)

    if node_id == 'net.fxarena.openfx.Text':
        custom = node.getParam('custom')
        custom_value = custom.get().replace(src_path, dst_path)
        if not custom.get() == custom_value:
            custom.set(custom_value)
