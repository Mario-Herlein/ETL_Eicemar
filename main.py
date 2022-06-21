import json
from ETL.Connection import Connection


with open("./config.json", "r") as f:
    config= json.load(f)

ENTORNO="PROD"
conexion = Connection(USER = config[ENTORNO]['user']
                    , PASS = config[ENTORNO]['pass']
                    , URLTOKEN = config[ENTORNO]['urlToken']
                    , REFERER = config[ENTORNO]['referer'] )

start='2022-05-29'
finish='2022-05-30'
mmsi="701078000"



busqueda=conexion.vesselSearch(mmsi,start,finish)




print("Busqueda")
a=busqueda["features"]
c=a[1]["attributes"]
print(c)
print(len(a))
print("Finalizado")
