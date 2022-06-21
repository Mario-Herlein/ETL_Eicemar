import requests
import time
import datetime as dt
import json
inicio = time.time()



with open('./config.json', 'r') as file:
    config = json.load(file, strict=False)


class Connection():
    USER=None
    PASS=None
    URLTOKEN=None
    API_HOST = None
    REFERER=None
    conn=None


    def __init__(self, USER,PASS,URLTOKEN,REFERER):
        self.USER=USER
        self.PASS=PASS
        self.URLTOKEN=URLTOKEN
        self.REFERER=REFERER

        self.payload = {
            "username": self.USER,
            "password": self.PASS,
            "client": "referer",
            "referer": self.REFERER,
            "expiration": "403120",
            "f": "pjson"
        }
        response= requests.request("POST",self.URLTOKEN,data=self.payload)
        token=response.json()
        print("Generando token")
        self.token = token["token"]

    def vesselSearch(self,mmsi,start,finish):
        token= self.token
        self.API_HOST=f"https://sig.prefecturanaval.gob.ar/apihost/rest/services/Realtime/positions_nmea/FeatureServer/0/query?f=json&token={token}&where=MMSI = '{mmsi}' AND msgTime > date '{start}' AND msgTime < date '{finish}'"
        response = requests.get(self.API_HOST)
        return response.json()



ENTORNO="PROD"
conexion = Connection(USER = config[ENTORNO]['user']
                    , PASS = config[ENTORNO]['pass']
                    , URLTOKEN = config[ENTORNO]['urlToken']
                    , REFERER = config[ENTORNO]['referer'] )

start='2022-04-30'
finish='2022-05-30'
token=conexion.token
mmsi="701078000"

busqueda=conexion.vesselSearch(mmsi,start,finish )

print("Busqueda")
a=busqueda["features"]
c=a[1]["attributes"]
print(c)
print(len(a))
print("Finalizado")
finish=dt.datetime.today()


fin = time.time()

print("Tiempo de ejecución", fin-inicio)