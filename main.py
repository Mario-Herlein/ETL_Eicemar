import logging
import json
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



    token=conexion.token
    start='2022-07-02'
    finish='2022-07-04'
    mmsi="701006867"



    busqueda=Search.trackSearch(token,mmsi,start,finish)


    df=Search.trackDataframe(busqueda)


    print(df.SOG.max())

    print(busqueda["positions"][-1])



if __name__ == '__main__':
    main()
