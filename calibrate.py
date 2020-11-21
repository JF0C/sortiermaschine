import json
import time
from statistics import mean
from pathlib import Path
from setservo import servo
from shaker import shaker
from colorscanner import colorscanner

servo1 = servo(23)
servo2 = servo(24)
shaker1 = shaker(25)
scanner = colorscanner(17, 27, 22, 5, 6, 26)
scanner.interval = 0.3
learn_rate = 0.2

def main():
  configfile = Path("./config.json")
  if not configfile.is_file():
    print("config file not found")
    with open("./config.json", "w") as file:
      json.dump({"pickup": 133, "scan": 100, "eject": 60, "shake_intens": 0.3, "shake_long": 1000, "shake_short": 500}, file)

  config = json.load(open("./config.json"))

  calfile = Path("./settings.json")
  if not calfile.is_file():
    with open("./settings.json", "w") as file:
      json.dump({}, file)

  data = json.load(open("./settings.json"))
  print("loaded: ")
  print(data)

  while True:
    servo1.turn(config["pickup"])
    shaker1.shake(config["shake_short"], config["shake_intens"])
    servo1.turn(config["scan"])
    time.sleep(0.3)
    cols = []
    for k in range(3):
      cols.append(scanner.readwrgb())
      shaker1.shake(500, 0.6)
    print(cols)
    color = []
    for k in range(4):
      color.append(mean([e[k] for e in cols]))
    print("measured " + str(color))
    print("please enter color name:")
    cname = input()
    if cname == "exit":
      servo2.turn_grad(0, 2)
      break
    if cname == "next":
      continue
    if cname in data:
      for k in range(4):
        data[cname][k] = data[cname][k] * (1-learn_rate) + color[k] * learn_rate
    else:
      data[cname] = color
      print("please enter angle in deg:")
      data[cname] = data[cname] + [int(input())]
    print(cname + ":")
    print(data[cname])
    servo2.turn_vel(data[cname][4], 30)
    servo1.turn(config["eject"])
    time.sleep(0.5)
    shaker1.shake(config["shake_short"], config["shake_intens"])
    time.sleep(0.5)
    with open("settings.json", "w") as file:
      json.dump(data, file, sort_keys=True, indent=4)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("aborting")
    shaker1.shake(1, 0.0)
    servo2.turn_grad(0, 2)
