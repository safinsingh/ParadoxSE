#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

echo """

██████╗  █████╗ ██████╗  █████╗ ██████╗  ██████╗ ██╗  ██╗███████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝██╔════╝██╔════╝
██████╔╝███████║██████╔╝███████║██║  ██║██║   ██║ ╚███╔╝ ███████╗█████╗  
██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║  ██║██║   ██║ ██╔██╗ ╚════██║██╔══╝  
██║     ██║  ██║██║  ██║██║  ██║██████╔╝╚██████╔╝██╔╝ ██╗███████║███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                         
"""

cd /opt

apt install -y git
apt install -y python3-pip

git clone https://github.com/safinsingh/ParadoxSE.git
cd ParadoxSE

pip3 install -r requirements.txt

echo "Performing cleanup..."
rm -rf /opt/ParadoxSE/docs/
rm -rf /opt/ParadoxSE/img/
rm -rf /opt/ParadoxSE/.gitattributes
rm -rf /opt/ParadoxSE/.gitignore
rm -rf /opt/ParadoxSE/.prettierignore
rm -rf /opt/ParadoxSE/.gitattributes
rm -rf /opt/ParadoxSE/install.sh
rm -rf /opt/ParadoxSE/README.md
rm -rf /opt/ParadoxSE/requirements.txt

echo "You can now configure scoring in the config.yml file"
