import os

path = '/usr/share/Natron/Plugins'
ignore = ['init', 'initGui']
ignore_folders = ['tools']

# Carga todos los modulos
for root, dirs, files in os.walk(path):
    for f in files:
        name = f.split('.')[0]
        ext = f.split('.')[-1]
        folder_name = os.path.basename(root)

        if not folder_name in ignore_folders:
            if not name in ignore:
                if ext == 'py':
                    exec('import ' + name)
