from natron_utils import createNode, getNode
import os

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate':
        create(thisNode, app)

def create(thisNode, app):
    videos_folder = thisNode.videos_dir.get()
    videos = os.listdir(videos_folder)

    merge = createNode('merge', 'merge', thisNode, position=[0, 300])

    left_photos = 4
    up_photos = 4
    scale = 1.0 / left_photos
    left_pos = 1920 / left_photos
    up_pos = 1080 * scale

    posx = 0

    left = 0
    conections = 3
    video_index = 0
    for l in range(left_photos):
        
        up = 0
        for u in range(up_photos):

            picture = videos_folder + '/' + videos[video_index]
            reader = app.createReader( picture, thisNode )
            reader.setPosition(posx, -300)

            name = str(l) + '-' + str(u)

            transform = createNode('transform', 'T' + name, thisNode, position=[posx, 0])
            transform.getParam('scale').set(scale, scale)
            transform.getParam('center').set(0,0)

            transform.getParam('translate').set(left, up)
            transform.connectInput(0, reader)
            
            conections += 1
            merge.connectInput(conections, transform)
            
            up += up_pos
            posx += 200
            video_index += 1

        left += left_pos
        
