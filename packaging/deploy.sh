#!/bin/bash
cd "$(dirname "$0")"
rsync -av --delete ../src/* systemd spetsnaz@shumeipai.local:/opt/homestuff/prom2unicornhathd
