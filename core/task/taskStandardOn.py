import os
os.system("cd /home/reyes/PycharmProjects/PP/task/")

if __name__ != "__main__":
    from core.classPin import *
else:
    from ..classPin import *

hPin = Pin()
hPin.send(13, 8)
hPin.send(12, 7)
hPin.send(11, 5)
hPin.send(8, 3)
hPin.send(7, 0)
