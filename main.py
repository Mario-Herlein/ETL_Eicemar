import logging
import json
import datetime as dt
from ETL.Extract import Connection , Search
from dateutil import parser


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

    start=str(dt.datetime.now()-dt.timedelta(days=30))
    finish=dt.datetime.now()
    mmsi="440528000"


    busqueda=Search.trackSearch(token, mmsi,start,str(finish))

    print(type(busqueda["positions"][-1]["msgTime"]))


    df=Search.trackDataframe(busqueda)


    print(df.SOG.max())

    # print(busqueda["positions"][-1])
    utc_dt=busqueda["positions"][-1]["msgTime"]
    print(type(utc_dt))
    # iso_date = parser.parse(utc_dt, tzinfos=None)
    # print('ISO datetime:', iso_date)

    # print('ISO datetime2:', iso_date.replace(tzinfo=None))

    # if iso_date.replace(tzinfo=None)<finish.replace(tzinfo=None):
    #     print("Faltan datos")
    # else:
    #     print("datos completos")


if __name__ == '__main__':
    print("Iniciando Nereo...")
    main()

