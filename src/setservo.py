import time
import RPi.GPIO as gpio
import sys

class servo:
  def __init__(self, pin):
    self.pin = pin
    self.pos = 0
    gpio.setmode(gpio.BCM)
    gpio.setup(self.pin, gpio.OUT)

  def turn(self, angle):
    angle %= 181
    self.pos = angle
    for k in range(5):
      self.send_angle(angle)

  def send_angle(self, angle):
    ton = 0.0004 + angle/181* 0.0021
    toff = 0.02 - ton
    for k in range(2):
      gpio.output(self.pin, gpio.HIGH)
      time.sleep(ton)
      gpio.output(self.pin, gpio.LOW)
      time.sleep(toff)

  def turn_vel(self, angle, deg_per_s):
    diff = angle - self.pos
    sec = diff/deg_per_s
    if sec < 0: sec *= -1
    self.turn_grad(angle, sec)

  def turn_grad(self, angle, sec):
    diff = angle - self.pos
    nsteps = int(sec*1000/20-5)
    angles = []
    for k in range(nsteps): angles.append(k/nsteps*diff + self.pos)
    for k in range(nsteps):
      self.send_angle(angles[k])
    for k in range(5): self.send_angle(angle)
    self.pos = angle

if __name__ == "__main__":
  if len(sys.argv) == 4:
    pin = int(sys.argv[1])
    angle = float(sys.argv[2])
    sec = float(sys.argv[3])
    s1 = servo(pin)
    s1.turn_grad(angle, sec)
  if len(sys.argv) < 3:
    print("specify pin and angle in deg [and seconds]")
  else:
    pin = int(sys.argv[1])
    angle = float(sys.argv[2])
    s1 = servo(pin)
    s1.turn(angle)


