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
start='2022-05-02'
finish='2022-07-04'
mmsi="701000516"



busqueda=Search.trackSearch(token,mmsi,start,finish) 


df=Search.trackDataframe(busqueda)


print(df)

print(busqueda["positions"][-1])

# posiciones=busqueda["positions"]



# # print(busqueda["positions"])

# print(len(posiciones))
# for index, a in enumerate(posiciones):
#     print("número de orden", index)
#     print("COG =", a['CourseOverGround'])
#     print("Time =", a["msgTime"])
#     print("Coordenadas =")
#     print("_____________Latitud: ",a["location"]["geo"]["coordinates"][1] )
#     print("_____________Longitud:",a["location"]["geo"]["coordinates"][0] )

# print(len(busqueda["positions"]))

# print("Busqueda")
# # a=busqueda["features"]
# # c=a[1]["attributes"]
# print(type(busqueda))
# # print(len(a))
# print("Finalizado")

# # print(conexion.token)