import os

path = '/usr/share/Natron/Plugins'
ignore = ['init', 'initGui']

# Carga todos los modulos
for root, dirs, files in os.walk(path):
    for f in files:
        name = f.split('.')[0]
        ext = f.split('.')[-1]

        if not name in ignore:
            if ext == 'py':
                exec('import ' + name)
