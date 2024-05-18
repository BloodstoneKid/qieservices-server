#!/bin/bash

tripwire --check > /opt/monitor/logs.txt
grep -i "$(date -d 'yesterday' +%Y-%m-%d)" /var/log/auth.log >> /opt/monitor/logs.txt
grep -i "$(date -d 'yesterday' +%Y-%m-%d)" /var/log/apache2/error.log >> /opt/monitor/logs.txt
grep -i "$(date -d 'yesterday' +%Y-%m-%d)" -A 5 /var/log/apt/history.log >> /opt/monitor/logs.txt
