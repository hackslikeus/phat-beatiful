#!/bin/bash 
bash
mkdir phatbeat
mkdir phatbeat/extras
cd phatbeat
git clone https://github.com/hackslikeus/phat-beatiful.git
mv index.html /var/www/index.html
mv demo_iframe.html /var/www/demo_iframe.html
mv phat-beatiful/extras/rpimonitor/data.conf /etc/rpimonitor
mv phat-beatiful/extras/rpimonitor/*.conf /etc/rpimonitor/template
mv phat-beatiful/extras/rpimonitor/*.png /usr/share/rpimonitor/web/img/
done
