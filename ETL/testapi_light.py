import requests
import json
import pandas as pd

url = "https://sig.prefecturanaval.gob.ar/apiadmin/track/get?f=json&token=amIGlAct2sCZm748XIePsvyj7d2NEpEcib8lZsdnI4r2camtjh2T4qD-rIzJgWqD_x2TWEZwd0agNpVNSJkOnlbJ9xg5MzEuZF5-chD8RBTMNq-uau61nZZI0X93Gf-595sUFPLdsdAmJZI1ehyptY9o1BVb4aV2O7bpIq-YildXqD5makiUgSR1_w-BzHD8SeOWz_-xmwgzmdO8eiacUA.."

payload = json.dumps({
  "ElementId": "Nyw5LDktT1RZeE1EQXlPRGMzTURVM05qSTNNa1pTUVU1RFNWTkRUdz09LU1UQTROemMxTURjME1URT0tYnVxdWU=",
  "from": "2022-06-21T08:30:00.000+00:00",
  "to": "2022-06-21T08:35:00.000+00:00",
  "includeH": True,
  "light": True,
  "addStatistics": True
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

#jsontr=response.json()["positions"]

#df2 = pd.read_json(jsontr, orient ='index')
#print(df2)
# for i in range(100):
#   fh=response.json()["positions"][i]["msgTime"]
#   fuente=response.json()["positions"][i]["feeder"]
#   print(f"FH : {fh} --------- Fuente: {fuente}")

print(response.json()["positions"][0])

