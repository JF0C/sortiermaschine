from setservo import servo
from shaker import shaker
import time

servo1 = servo(23)
shaker1 = shaker(25)
servo1.turn(133)
time.sleep(0.5)
shaker1.shake(1000, 1.0)
servo1.turn(80)
time.sleep(0.5)
servo1.turn(100)
time.sleep(2)
servo1.turn(50)
shaker1.shake(500, 1.0)
time.sleep(2)
servo1.turn(133)
