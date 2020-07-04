#! /usr/bin/sh

natron_plugins='/usr/share/Natron/Plugins'
mkdir -p $natron_plugins

rm -rf $natron_plugins/*

# copia el core a la carpeta plugins de natron
cp core/* $natron_plugins
cp plugins/* $natron_plugins

chmod 777 -R $natron_plugins
