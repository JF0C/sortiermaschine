import json
import time
from pathlib import Path
from setservo import servo
from shaker import shaker
from colorscanner import colorscanner


servo1 = servo(23)
servo2 = servo(24)
shaker1 = shaker(25)
scanner = colorscanner(17, 27, 22, 5, 6, 26)
scanner.interval = 0.3

def main():
  configfile = Path("./config.json")
  if not configfile.is_file():
    print("config file not found")
    with open("./config.json", "w") as file:
      json.dump({"pickup": 133, "scan": 100, "eject": 60, "shake_intens": 0.3, "shake_short": 500, "shake_long": 1000}, file)

  config = json.load(open("./config.json"))

  if not Path("./settings.json").is_file():
    print("settins.json not found\nplease calibrate first")

  data = json.load(open("./settings.json"))
  print("loaded: ")
  print(data)

  while True:
  #  if input() == "exit":
  #    break
    servo1.turn(config["pickup"])
    shaker1.shake(config["shake_long"], config["shake_intens"])
    servo1.turn(config["scan"])
    time.sleep(0.3)
    color = scanner.readwrgb()
    for n in range(5):
      for k in range(3):
        color[k] /= color[3]
      cname = ""
      best_approx = 1000
      for k in data:
        approx = 0
        for l in range(3):
          approx += (color[l] - data[k][l]/data[k][3])**2
        if approx < best_approx:
          best_approx = approx
          cname = k
      if best_approx < 0.0025: break

    if best_approx > 0.005:
      print("color not found")
      servo2.turn(config["notfound"])
      #servo2.turn_vel(positions["notfound"], 30)
    else:
      print("found color " + cname + " with error " + str(best_approx))
      #servo2.turn_vel(data[cname][4], 30)
      servo2.turn(data[cname][4])
    time.sleep(0.5)
    servo1.turn(config["eject"])
    shaker1.shake(config["shake_short"], config["shake_intens"])
    time.sleep(0.5)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("aborting")
    shaker1.shake(1, 0.0)
    servo2.turn_grad(0, 2)
