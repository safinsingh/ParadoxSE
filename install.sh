#!/bin/bash

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

echo "/usr/bin/python3 /opt/ParadoxSE/worker.py" > /usr/local/bin/score
chmod +x /usr/local/bin/score