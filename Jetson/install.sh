#! /bin/bash

#get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#get the current user
USER=$(whoami)

#copy thecultivator.service file to /etc/systemd/system
sudo cp $DIR/thecultivator.service /etc/systemd/system/

#replace in thecultivator.service file ##PATH## with the current directory
sudo sed -i "s|##PATH##|$DIR|g" /etc/systemd/system/thecultivator.service

#replace in thecultivator.service file ##USER## with the current user
sudo sed -i "s|##USER##|$USER|g" /etc/systemd/system/thecultivator.service

#copy stepmotors.service file to /etc/systemd/system
sudo cp $DIR/stepmotors.service /etc/systemd/system/

#replace in stepmotors.service file ##PATH## with the current directory
sudo sed -i "s|##PATH##|$DIR|g" /etc/systemd/system/stepmotors.service

#make stepMotor
cd $DIR/stepMotors
make

#reload systemd
sudo systemctl daemon-reload

#enable stepmotors.service
sudo systemctl enable stepmotors.service

#start stepmotors.service
sudo systemctl start stepmotors.service

#enable thecultivator.service
sudo systemctl enable thecultivator.service

#start thecultivator.service
sudo systemctl start thecultivator.service