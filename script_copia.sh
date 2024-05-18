#!/bin/bash

fecha=`date +%Y%m%d`

tar czf /opt/copias/copia-$fecha.tar.gz /etc /var/www /home /usr/lib/cgi-bin
