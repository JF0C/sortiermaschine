import time
import RPi.GPIO as gpio
import sys
import numpy as np


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
    self.samplefreq = 1000
    self.nrsamples = 100


  def readpwm(self):
    signal = np.zeros((self.nrsamples, 2))

    gpio.output(self.oe, gpio.HIGH)
    t_last = time.time()

    for i in np.range(0, self.nrsamples):
      while (time.time() < t_last + 1/self.samplefreq):
        #set frequency
        k=0


      t_last = time.time()
      signal[i, 0] = gpio.input(self.fin)
      signal[i, 1] = t_last


    gpio.output(self.oe, gpio.LOW)
    return signal

  def readwrgb(self):
    result = np.zeros(4)

    gpio.output(self.s0, gpio.LOW)
    gpio.output(self.s1, gpio.HIGH)

    # read white
    gpio.output(self.s2, gpio.HIGH)
    gpio.output(self.s3, gpio.LOW)
    signal = self.readpwm()
    amp_dB = np.abs(np.fft.fft(signal[:,0]))
    freq_Hz = np.fft.fftfreq(signal[:,1].shape[-1])
    amp_dB = amp_dB[freq_Hz>0]
    freq_Hz = freq_Hz[freq_Hz>0]
    result[0] = freq_Hz[np.argmax(amp_dB)]

    # read red
    gpio.output(self.s2, gpio.LOW)
    gpio.output(self.s3, gpio.LOW)
    signal = self.readpwm()
    amp_dB = np.abs(np.fft.fft(signal[:,0]))
    freq_Hz = np.fft.fftfreq(signal[:,1].shape[-1])
    amp_dB = amp_dB[freq_Hz>0]
    freq_Hz = freq_Hz[freq_Hz>0]
    result[1] = freq_Hz[np.argmax(amp_dB)]

    # read green
    gpio.output(self.s2, gpio.HIGH)
    gpio.output(self.s3, gpio.HIGH)
    signal = self.readpwm()
    amp_dB = np.abs(np.fft.fft(signal[:,0]))
    freq_Hz = np.fft.fftfreq(signal[:,1].shape[-1])
    amp_dB = amp_dB[freq_Hz>0]
    freq_Hz = freq_Hz[freq_Hz>0]
    result[2] = freq_Hz[np.argmax(amp_dB)]

    # read blue
    gpio.output(self.s2, gpio.LOW)
    gpio.output(self.s3, gpio.HIGH)
    signal = self.readpwm()
    amp_dB = np.abs(np.fft.fft(signal[:,0]))
    freq_Hz = np.fft.fftfreq(signal[:,1].shape[-1])
    amp_dB = amp_dB[freq_Hz>0]
    freq_Hz = freq_Hz[freq_Hz>0]
    result[3] = freq_Hz[np.argmax(amp_dB)]

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

