import json
from ETL.Extract import Connection , Search


with open("./config.json", "r") as f:
    config= json.load(f)

ENTORNO="PROD"
conexion = Connection(USER = config[ENTORNO]['user']
                    , PASS = config[ENTORNO]['pass']
                    , URLTOKEN = config[ENTORNO]['urlToken']
                    , REFERER = config[ENTORNO]['referer'] )



token=conexion.token
start='2022-07-02'
finish='2022-07-04'
mmsi="412334077"



busqueda=Search.trackSearch(token,mmsi,start,finish) 




print(busqueda)

print("Busqueda")
# a=busqueda["features"]
# c=a[1]["attributes"]
print(type(busqueda))
# print(len(a))
print("Finalizado")

# print(conexion.token)