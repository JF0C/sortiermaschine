import time
import RPi.GPIO as gpio
import sys

class shaker:
  def __init__(self, pin):
    self.lowactive = True
    self.pin = pin
    gpio.setmode(gpio.BCM)
    gpio.setup(self.pin, gpio.OUT)
    if self.lowactive:
      gpio.output(self.pin, gpio.HIGH)

  def shake(self, ms, intens):
    if intens > 1.0: intens = 1.0
    if intens < 0.0: intens = 0.0
    ton = 0.01 * intens
    toff = 0.01 * (1-intens)
    on = False
    elapsed = 0
    while elapsed < ms:
      if on:
        self.set(True)
        time.sleep(ton)
        elapsed += 1000*ton
      else:
        self.set(False)
        time.sleep(toff)
        elapsed += 1000*toff
      on = not on
    self.set(False)

  def set(self, value):
    if self.lowactive:
      gpio.output(self.pin, not value)
    else:
      gpio.output(self.pin, value)

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("specify pin, ms and intensity")
  else:
    pin = int(sys.argv[1])
    ms = int(sys.argv[2])
    intens = float(sys.argv[3])
    s1 = shaker(pin)
    s1.shake(ms, intens)
