#!/bin/bash
# laser_sysfs.sh – zapisz jako plik, chmod +x, sudo ./laser_sysfs.sh

echo 12 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio12/direction

while true; do
    echo 0 > /sys/class/gpio/gpio12/value; sleep 1    # 0%
    for i in {0..50}; do echo 1 > /sys/class/gpio/gpio12/value; sleep 0.00001; echo 0 > /sys/class/gpio/gpio12/value; sleep 0.001; done; sleep 1  # ~5% (software PWM)
    for i in {0..100}; do echo 1 > /sys/class/gpio/gpio12/value; sleep 0.00001; echo 0 > /sys/class/gpio/gpio12/value; sleep 0.001; done; sleep 1  # ~10%
done

