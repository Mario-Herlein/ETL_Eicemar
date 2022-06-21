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
            start (date): Fecha desde donde comienza la busqueda
            finish (date): Fecha hasta donde finaliza la busqueda

        Returns:
            json:Contiene todos los datos de posiciones del buque, incluidas las fuentes de datos
        """
        token= self.token
        self.API_HOST=f"https://sig.prefecturanaval.gob.ar/apihost/rest/services/Realtime/positions_nmea/FeatureServer/0/query?f=json&token={token}&where=MMSI = '{mmsi}' AND msgTime > date '{start}' AND msgTime < date '{finish}'"
        response = requests.get(self.API_HOST)
        return response.json()



