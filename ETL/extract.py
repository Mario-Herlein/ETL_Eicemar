import logging
import pandas as pd
import requests
import json
from tqdm import tqdm
from dateutil import parser
import traceback




with open('./config.json', 'r') as file:
    config = json.load(file, strict=False)


class Connection():
    """
    This Class allows connecting to the API that connects to the GC3 DB
    """

    def __init__(self, USER,PASS,URLTOKEN,REFERER):
        self.USER=USER
        self.PASS=PASS
        self.URLTOKEN=URLTOKEN
        self.REFERER=REFERER

    def token(self):
        self.payload = {
            "username": self.USER,
            "password": self.PASS,
            "client": "referer",
            "referer": self.REFERER,
            "expiration": "403120",
            "f": "pjson"
        }
        response= requests.request("POST",self.URLTOKEN,data=self.payload)
        i=0
        while i<5:
            try:
                token=response.json()
                self.token = token["token"]
                logging.info(f"INFO Generando token: {self.token}")
                return self.token
            except:
                self.token=response.json()["error"]
                logging.warning(f"WARNING token no generado {self.token}")
                i+=1
        logging.warning("ERROR Luego de 5 intentos no se puedo conectar a la API")


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
        print("Buscando elementId")
        logging.info("INFO - Buscando elementId")
        try:
            url = "https://sig.prefecturanaval.gob.ar/apiadmin/elements/search?f=json"
            response = requests.request("POST", url, headers=headers, data=payload)
            elementId=response.json()[0]["elementId"]
            return elementId
        except ValueError:
                logging.critical("CRITICAL - La API no responde correctamente, 'requests.exceptions.JSONDecodeError'")
                print("CRITICAL - La API no responde correctamente, 'requests.exceptions.JSONDecodeError'")
                return None
        except IndexError:
                logging.error(f"ERROR - MMSI {mmsi} not found")
                print(f"ERROR - MMSI {mmsi} not found")
                return None

    def trackSearch(token:None,mmsi,desde,hasta):
        """  Using API connection, look up vessel positions by MMSI, according to given dates
        Args:
            mmsi (str): MMSI number of the vessel to search
            from (datetime): Date from where the search starts
            finish (datetime): Date until where the search ends

        returns:
            json: Contains all position data of the ship, including data sources
        """
        ElementId=Search.vessel_by_Mmsi(mmsi)
        if ElementId:
            url=f"https://sig.prefecturanaval.gob.ar/apiadmin/track/get?f=json&token={token}"
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
            try:
                respuesta= response.json()
                return respuesta
            except ValueError:
                logging.critical("CRITICAL - La API no responde correctamente, 'requests.exceptions.JSONDecodeError'")
                print("CRITICAL - La API no responde correctamente, 'requests.exceptions.JSONDecodeError'")
                return None
        else:
            print("No se encontró el elementID")


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
            msgTime=parser.parse(pos["msgTime"], ignoretz=True)
            position={"FH":msgTime,
                       "SOG":pos['SpeedOverGroud'],
                       "COG":pos['CourseOverGround']}
            try:
                        position.update({"X":pos["location"]["geo"]["coordinates"][0],
                 "Y":pos["location"]["geo"]["coordinates"][1]})

            except KeyError:
                list_KeyError.append(pos['objectId'])
                continue

            list_positions.append(position)
        df=pd.DataFrame(list_positions)

        logging.info(f"INFO - Porcentaje de ObjectId sin coordenadas:{round((len(list_KeyError)*100)/len(df),2)}%" )

        return df





