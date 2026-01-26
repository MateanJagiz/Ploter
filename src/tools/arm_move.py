import RPi.GPIO as GPIO
import json
from time import sleep
import argparse
from module.instruction import make_instruction as make
from module.utils import *

# ==================================  ARRANGE  ==================================

laser_on()
sleep(5)
laser_off()
for i in range(1000):
    active_step()
laser_on()
sleep(5)
laser_off()

