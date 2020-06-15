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

echo "You can now configure scoring in the config.yml file"
