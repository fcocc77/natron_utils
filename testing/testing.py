
import sys
from sys import argv
import NatronEngine


from videovina import get_slides

project = '/home/pancho/Documents/GitHub/videovina/private/templates_base/base/comp/base.ntp'

app.loadProject(project)
slides = get_slides(app)

# datos correctos
slide_amount = 5
_format = 1  # quarter, half, hd, 4k
speed = 0  # Slow, Normal, Fast
# -------------------


def testing(message, fact, hoped=None, error=None):
    if hoped:
        if fact == hoped:
            print '- ' + message + ': OK'
        else:
            print '- ' + message + ': ERROR ( testing: ' + str(fact) + ' y deberia ser: ' + str(hoped) + ' )'
    else:
        if fact:
            print '- ' + message + ': OK'
        else:
            print '- ' + message + ': ERROR ( ' + error + ' )'


def slide_testing(message, error):
    testing(message, False if error else True,
            error='Nodos con error: ' + error)


format_error = ''
speed_error = ''
for i, slide in enumerate(slides):
    transition = slide['transition']
    if not transition.getParam('format').get() == _format:
        format_error += transition.getLabel() + ', '

    if not transition.getParam('speed').get() == speed:
        speed_error += transition.getLabel() + ', '

testing('Cantidad de slides', len(slides), slide_amount)
slide_testing('Formato', format_error)
slide_testing('Speed', speed_error)
