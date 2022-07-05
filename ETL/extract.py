from xml.dom.minidom import Element
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
        


class Search():
    
    
    def vessel_by_Mmsi(mmsi):
        """Usando la API Arcgis, para buscar el ID de elementos"

        Args:
            mmsi (string): 

        Returns:
            _type_: _description_
        """        
        mmsi = str(mmsi)
        payload = json.dumps({"criteria": {"MMSI": mmsi,"elementType": "buque"}})
        headers = {'Content-Type': 'application/json'}
        try:
            url = "https://sig.prefecturanaval.gob.ar/apiadmin/elements/search?f=json"
            response = requests.request("POST", url, headers=headers, data=payload)
            elementId=response.json()[0]["elementId"]
            return elementId

        except:
            print(f"MMSI {mmsi} not found")
            return None
    
    def trackSearch(token,mmsi,desde,hasta):
        """  Usando la conexión a la API, busca las posiciones del buque por MMSI, acorde las fechas determinadas
        Args:
            mmsi (str): Numero MMSI del buque a buscar
            from (datetime): Fecha desde donde comienza la busqueda
            finish (datetime): Fecha hasta donde finaliza la busqueda

        Returns:
            json:Contiene todos los datos de posiciones del buque, incluidas las fuentes de datos """
        
        url=f"https://sig.prefecturanaval.gob.ar/apiadmin/track/get?f=json&token={token}"
        ElementId=Search.vessel_by_Mmsi(mmsi)
        payload = json.dumps({"ElementId": ElementId,
        "from": desde,
        "to": hasta,
        "includeH": True,
        "light": True,
        "addStatistics": True
        })
        headers = {'Content-Type': 'application/json'}
        
        response = requests.request("POST", url, headers=headers, data=payload)
        print("Buscando Posiciones")
        
        return response.json()