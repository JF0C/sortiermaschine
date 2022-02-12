import time
import RPi.GPIO as gpio
import sys


class colorscanner:
  def __init__(self, s0, s1, s2, s3, oe, fin):
    self.s0 = s0
    self.s1 = s1
    self.s2 = s2
    self.s3 = s3
    self.oe = oe
    self.fin = fin
    gpio.setmode(gpio.BCM)
    gpio.setup(self.s0, gpio.OUT)
    gpio.setup(self.s1, gpio.OUT)
    gpio.setup(self.s2, gpio.OUT)
    gpio.setup(self.s3, gpio.OUT)
    gpio.setup(self.oe, gpio.OUT)
    gpio.setup(self.fin, gpio.IN)
    self.interval = 1

  def readpwm(self):
    t_start = time.time()
    count = 0
    value = 0
    gpio.output(self.oe, gpio.HIGH)
    while time.time() < t_start + self.interval:
      if gpio.input(self.fin) and not value:
        count += 1
        value = 1
      elif not gpio.input(self.fin) and value:
        value = 0
    gpio.output(self.oe, gpio.LOW)
    return count

  def readwrgb(self):
    result = [0, 0, 0, 0]

    gpio.output(self.s0, gpio.LOW)
    gpio.output(self.s1, gpio.HIGH)

    # read white
    gpio.output(self.s2, gpio.HIGH)
    gpio.output(self.s3, gpio.LOW)
    result[0] = self.readpwm()

    # read red
    gpio.output(self.s2, gpio.LOW)
    gpio.output(self.s3, gpio.LOW)
    result[1] = self.readpwm()

    # read green
    gpio.output(self.s2, gpio.HIGH)
    gpio.output(self.s3, gpio.HIGH)
    result[2] = self.readpwm()

    # read blue
    gpio.output(self.s2, gpio.LOW)
    gpio.output(self.s3, gpio.HIGH)
    result[3] = self.readpwm()

    return result

  def getinterval(self):
    return self.interval

  def setinterval(self, val):
    self.interval = val

if __name__ == "__main__":
  sc1 = colorscanner(17, 27, 22, 5, 6, 26)
  res = [0, 0, 0, 0]
  print("scanning")
  while(True):
    res = sc1.readwrgb()
    msg = "col("
    for k in range(4):
      res[k] = res[k] / sc1.interval * 50 / 1000
      msg += str(res[k]) + ", "
    msg = msg[0:-2]
    msg += ")"
    print(msg)
    break

