#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo 'This script must be run as root'
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

read -p "Are you sure you wish to continue? (yes/no)" res
if [ "${res,,}" != "yes" ]; then
   exit
fi

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

echo "* * * * * root /usr/bin/python3 /opt/ParadoxSE/worker.py" > /etc/crontab

echo """
if [[ $EUID -ne 0 ]]; then
   echo 'This script must be run as root'
   exit 1
fi

/usr/bin/python3 /opt/ParadoxSE/worker.py
""" > /usr/local/bin/score

chmod +x /usr/local/bin/score

if grep -Fxq "production=True" worker.py; then
    read -p """You are running ParadoxSE in production mode. 
    This means it will delete the config.yml file. Please back it up
    and then press enter to proceed"""
    rm -f config.yml
fi
