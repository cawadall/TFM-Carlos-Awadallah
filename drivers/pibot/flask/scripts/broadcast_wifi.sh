#!/bin/bash

sudo sed '4,$d' -i /etc/wpa_supplicant/wpa_supplicant.conf


wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap

