import json

data = json.load(open("settings.json"))
for k in data:
  print(k + ":")
  print("r=" + str(data[k][0]/data[k][3]) +
        " g=" + str(data[k][1]/data[k][3]) +
        " b=" + str(data[k][2]/data[k][3]))


