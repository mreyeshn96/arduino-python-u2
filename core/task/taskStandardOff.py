#!/usr/bin/python3.8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classPin import *

hPin = Pin()
hPin.send(13, 9)
hPin.send(12, 6)
hPin.send(11, 4)
hPin.send(8, 2)
hPin.send(7, 1)
