#! /usr/bin/sh

natron_plugins='/usr/share/Natron/Plugins'
mkdir -p $natron_plugins

# copia el core a la carpeta plugins de natron
cp core/* $natron_plugins

chmod 777 -R $natron_plugins
