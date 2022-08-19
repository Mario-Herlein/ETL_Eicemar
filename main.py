from operator import index
import pandas as pd
import logging
import json
import datetime as dt
from datetime import datetime
from ETL.Extract import Connection , Search
from ETL.Transform import Transform


def main():
    """
    It reads a json file, then it creates a connection object, then it gets a token, then it gets a
    start and finish date, then it gets a mmsi.
    """
    logging.basicConfig(filename="logsdesa/nereo.log", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO)
    logging.info("INFO Iniciando Nereo")

    with open("./config.json", "r") as f:
        config= json.load(f)

    ENTORNO="PROD"
    conexion = Connection(USER = config[ENTORNO]['user']
                        , PASS = config[ENTORNO]['pass']
                        , URLTOKEN = config[ENTORNO]['urlToken']
                        , REFERER = config[ENTORNO]['referer'] )

    token= conexion.token()

    """Las horas son ingresadas en UTC pero devuelve en local"""
    start= "2022-08-12T09:30:00.000+00:00"#str(dt.datetime.now()-dt.timedelta(days=1))#"2022-08-12T05:00:00.000+00:00"#
    finish="2022-08-12T12:00:00.000+00:00"#str(dt.datetime.now()) #"2022-08-12T10:00:00.000+00:00"#
    mmsi= "701000652"#"701006744"
    
    busqueda=Search.trackSearch(token, mmsi,start,finish)

    # print(type(busqueda["positions"][-1]["msgTime"]))

    df=Search.trackDataframe(busqueda)
    print(df.shape)

    if df.empty:
        logging.info("INFO - El buque no tiene posiciones")
        print("El buque no tiene posiciones")
        return None

    start =dt.datetime.now()
    df_mod=Transform.addNewCols(df)
    finish = dt.datetime.now()

    print(finish - start)
    # last_register=df.iloc[-1]["FH"]
    # print(df.SOG.max())

    # print(last_register)
    # print(busqueda["positions"][-1])
    # iso_date = parser.parse(utc_dt, ignoretz=True)
    # print('ISO datetime:', iso_date)

    # print('ISO datetime2:', iso_date.replace(tzinfo=None))

    # if last_register<finish.replace(tzinfo=None):
    #     print("Faltan datos")
    # else:
    #     print("datos completos")
    return df_mod


if __name__ == '__main__':
    # a=main()
    # df=a[["FH","SOG","COG","X","Y"]]
    # print(a.shape)
    # print(df)
    df1=pd.read_csv("maraustral.csv", delimiter=";")
    # print(df1)
    df1["FH"]=pd.to_datetime(df1["FH"], format='%d/%m/%Y %H:%M')
    df1=Transform.addNewCols(df1)
    # print(df1)
    df=df1[["FH","SOG","COG","X","Y"]]
    print(df)
    df["NOMBRE"]="Mar Austral I"

    df.to_csv("MARAUSTRALI.csv", index=False)