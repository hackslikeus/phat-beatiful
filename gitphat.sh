#!/bin/bash 
bash
mkdir phatbeat
mkdir phatbeat/extras
cd phatbeat
git clone https://github.com/hackslikeus/phat-beatiful.git
mv index.html /var/www/index.html
mv demo_iframe.html /var/www/demo_iframe.html
mv phatbeat/extras/rpimonitor/data.conf /etc/rpimonitor
mv phatbeat/extras/rpimonitor/*.conf /etc/rpimonitor/template
mv phatbeat/extras/rpimonitor/*.png /usr/share/rpimonitor/web/img/
mv radio.m3u /mnt/dietpi_userdata/Music/
cp /etc/asound.conf /etc/oldasound.conf
mv use_asound.conf /etc/asound.conf
done
