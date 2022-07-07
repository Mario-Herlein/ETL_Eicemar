import logging
import pandas as pd
import requests
import json
from tqdm import tqdm




with open('./config.json', 'r') as file:
    config = json.load(file, strict=False)


class Connection():
    """
    This Class allows connecting to the API that connects to the GC3 DB
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
        self.token = token["token"]
        logging.info(f"Generando token: {self.token}")
        print("Generando token")
        


class Search():


    def vessel_by_Mmsi(mmsi):
        """Using the Arcgis API, to look up the ID of elements"

        Args:
            mmsi (string):MMSI number of the vessel to search

        Returns:
            elementId(string): the unique ID of elements in th db
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
        """  Using API connection, look up vessel positions by MMSI, according to given dates
        Args:
            mmsi (str): MMSI number of the vessel to search
            from (datetime): Date from where the search starts
            finish (datetime): Date until where the search ends

        returns:
            json: Contains all position data of the ship, including data sources
        """

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
        print("Buscando Posiciones")
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()


    def trackDataframe(json):
        """
        It takes a json file, loops through it, and creates a dataframe with the data
        
        :param json: the json file
        :return: A dataframe with the following columns:
        FH, SOG, COG, X, Y
        """
        positions=json["positions"]
        list_positions=[]
        list_KeyError=[]
        position={}

        for pos in tqdm(positions):
            position={"FH":pos["msgTime"],
                       "SOG":pos['SpeedOverGroud'],
                       "COG":pos['CourseOverGround']}
            try:
                        position.update({"X":pos["location"]["geo"]["coordinates"][0],
                 "Y":pos["location"]["geo"]["coordinates"][1]})

            except KeyError:
                # print( f" El ObjectId {pos['objectId']}, no tiene coordenadas")
                list_KeyError.append(pos['objectId'])
                continue

            list_positions.append(position)
        df=pd.DataFrame(list_positions)

        print("Porcentaje de ObjectId sin coordenadas: ", round((len(list_KeyError)*100)/len(df),2),"%" )

        return df





