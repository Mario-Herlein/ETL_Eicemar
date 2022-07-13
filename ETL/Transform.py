import pandas as pd
from geographiclib.geodesic import Geodesic
from tqdm.notebook import tqdm_notebook

class Transform:


    def getDistCog(lat1, long1, lat2, long2):
        """
        It takes two sets of lat/long coordinates and returns the distance between them in nautical miles
        and the course over ground (COG) in degrees

        :param lat1: latitude of the first point
        :param long1: longitude of the first point
        :param lat2: latitude of the destination point
        :param long2: longitude of the destination
        :return: The distance and the course over ground (COG)
        """
        geodata = Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)
        dist=geodata['s12']/1852
        cog=geodata["azi1"]
        if cog<0:
            cog+=360
        return dist,cog

    def addNewCols(df):
        max_SOG=df.SOG.max()
        row=0
        pbar = tqdm_notebook(total=len(df))
        while row<len(df)-1:
            pbar.update(row)
            indice=row+1
            tiempo=(df.loc[indice,'FH']-df.loc[row,'FH']).total_seconds()
            dist,cog=getDistCog( df.loc[row, "Y"],df.loc[row, "X"]  , df.loc[indice, "Y"], df.loc[indice, "X"])
            knots= dist/(tiempo/3600)
            # Si la velocidad calculada es mayor a la velocidad máxima registrada por el buque, recalculo con la siguiente posición
            while knots>max_SOG:
                df.loc[indice,"SOG_mean"]="NaN"
                indice+=1
                if indice<len(df)-1:
                    tiempo=(df.loc[indice,'FH']-df.loc[row,'FH']).total_seconds()
                    dist,cog=getDistCog(df.loc[row, "Y"],df.loc[row, "X"]  , df.loc[indice, "Y"], df.loc[indice, "X"])
                    knots=dist/(tiempo/3600)
                else:
                    break
            else:
                row=indice
                df.loc[indice,"SOG_mean"]=knots
                df.loc[indice,"DISTANCIA_Nm"]=dist
                df.loc[indice,"COG_mean"]=cog
                df.loc[indice,"STEP"]=tiempo
        pbar.close()