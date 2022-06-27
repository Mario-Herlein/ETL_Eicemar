import requests
import json


def vessel_by_Mmsi(mmsi):
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
    
    #def vessel_by_Id(self, token, element_id):

