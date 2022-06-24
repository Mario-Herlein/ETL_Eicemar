import requests
import json




with open('./config.json', 'r') as file:
    config = json.load(file, strict=False)


class Connection():
    """
    Esta Clase permite conectarse a la API  que se conecta a la BDD del GC3
    """
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
        """Usando la conexión a la API, busca
        las posiciones del buque por MMSI, acorde las fechas determinadas

        Args:
            mmsi (str): Numero MMSI del buque a buscar
            start (datetime): Fecha desde donde comienza la busqueda
            finish (datetime): Fecha hasta donde finaliza la busqueda

        Returns:
            json:Contiene todos los datos de posiciones del buque, incluidas las fuentes de datos
        """
        json={    "ElementId" : "Nyw5LDktT1RZeE1EQXlPRGMzTURVM05qSTNNa1pTUVU1RFNWTkRUdz09LU1UQTROemMxTURjME1URT0tYnVxdWU=",
    "from" : "2022-03-01T08:30:00.000+00:00",
    "to" : "2022-03-03T18:30:00.000+00:00",
    "includeH" : True,
    "addStatistics" : True}
        token= self.token
        self.API_HOST=f"https://sig.prefecturanaval.gob.ar/apiadmin/track/get?f={json}&token={token}"
        response = requests.get(self.API_HOST)
        print(response)
        print(token)
        return response.json()

 # https://sig.prefecturanaval.gob.ar/apiadmin/track/get

# f"https://sig.prefecturanaval.gob.ar/apihost/rest/services/Realtime/positions_nmea/FeatureServer/0/query?f=json&token={token}&where=MMSI = '{mmsi}' AND msgTime > date '{start}' AND msgTime < date '{finish}'"

