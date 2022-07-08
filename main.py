import logging
import json
import datetime as dt
from ETL.Extract import Connection , Search


def main():
    """
    It reads a json file, then it creates a connection object, then it gets a token, then it gets a
    start and finish date, then it gets a mmsi.
    """
    logging.basicConfig(filename="logsdesa/nereo.log", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO)
    logging.info("Iniciando Nereo")

    with open("./config.json", "r") as f:
        config= json.load(f)

    ENTORNO="PROD"
    conexion = Connection(USER = config[ENTORNO]['user']
                        , PASS = config[ENTORNO]['pass']
                        , URLTOKEN = config[ENTORNO]['urlToken']
                        , REFERER = config[ENTORNO]['referer'] )


    
    token= conexion.token()

    start=str(dt.datetime.now()-dt.timedelta(days=1))
    finish=str(dt.datetime.now())
    mmsi="440528000"


    busqueda=Search.trackSearch(token, mmsi,start,finish)


    df=Search.trackDataframe(busqueda)


    print(df.SOG.max())

    # print(busqueda["positions"][-1])
    # print(type(dt.datetime.strptime(busqueda["positions"][-1]["msgTime"], '%Y-%m-%d %H:%M:%S.%f')))



if __name__ == '__main__':
    print("Iniciando Nereo...")
    main()

