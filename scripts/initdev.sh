#!/bin/bash

dir_scripts=$(cd $(dirname $0); pwd)
dir_project=$(dirname $dir_scripts)

pip3 install -r $dir_scripts/py-requirements.txt
for extension in $(cat $dir_scripts/vscode-recommendations.txt); do
    code --install-extension $extension
done

mkdir -p ~/.config/
mkdir -p ~/.config/gdb/
echo "set auto-load safe-path /" >> ~/.config/gdb/gdbinit

cd $dir_project
make -C $dir_scripts/agent-proxy/

cd $dir_project/visualizer/
source $dir_scripts/node_install.sh
