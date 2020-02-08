#!/bin/bash

sudo cp wpa_supplicant.conf /etc/wpa_supplicant
sudo cp dhcpcd.conf /etc/
sudo service dhcpcd restart

