#!/usr/bin/python3.8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classPin import *
hPin = Pin()
hPin.send(13, 8)
hPin.send(12, 7)
hPin.send(11, 5)
hPin.send(8, 3)
hPin.send(7, 0)
