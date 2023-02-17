#!/usr/bin/env python

import time
import unicornhathd
import requests
import re

unicornhathd.clear()
unicornhathd.brightness(0.1)
unicornhathd.rotation(270)
dummies = [200, 500, 300]
values = []
max_samples = 16
resolution = 16
try:
    while True:
        response = requests.get('http://localhost:9100/metrics')
        if response.status_code == 200:
            result = re.search(r"\npv_ac_energy_watt (\d+)\n", response.text)
            if result != None:
                print(result.groups())
                pv_ac_energy_watt = int(result.group(1))
                print("Power = ", pv_ac_energy_watt, "W")
                values.insert(0, pv_ac_energy_watt)
            else:
                values.insert(0, 0) 
        else: 
            values.insert(0, 0) 
            print("unexpected response code", response.status_code)

        if len(values) == max_samples:
            del values[max_samples - 1]

        # print("values", values)
        max_value = max(values)
        scaling_factor = max(1, max_value / resolution) 

        pos = max_samples - 1 #go from right to left
        unicornhathd.clear()
        for value in values:
            # print("Updating position ", pos, " with value: ", value)
            pixels = round(value / scaling_factor)
            for p in range(pixels):
                unicornhathd.set_pixel(pos, p, 0, 255, 0)
            pos = pos - 1
        unicornhathd.show()
        time.sleep(60)

except KeyboardInterrupt:
    unicornhathd.off()
