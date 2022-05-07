#! /bin/bash

#get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#copy thecultivator.service file to /etc/systemd/system
sudo cp $DIR/thecultivator.service /etc/systemd/system/

#replace in thecultivator.service file ##PATH## with the current directory
sudo sed -i "s|##PATH##|$DIR|g" /etc/systemd/system/thecultivator.service

#reload systemd
sudo systemctl daemon-reload

#enable thecultivator.service
sudo systemctl enable thecultivator.service

#start thecultivator.service
sudo systemctl start thecultivator.service