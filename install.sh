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

apt install git
apt install python3-pip

git clone https://github.com/safinsingh/ParadoxSE.git
cd ParadoxSE

pip3 install -r requirements.txt

echo "* * * * * root /usr/bin/python3 /opt/ParadoxSE/worker.py" > /etc/crontab

echo """
if [[ $EUID -ne 0 ]]; then
   echo 'This script must be run as root'
   exit 1
fi

/usr/bin/python3 /opt/ParadoxSE/worker.py
""" > /usr/local/bin/score

chmod +x /usr/local/bin/score
