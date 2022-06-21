
from ETL.Connection import vesseSearch 



start='2022-04-30'
finish='2022-05-30'
mmsi="701078000"



vesselSearch(mmsi,start,finish)




print("Busqueda")
a=busqueda["features"]
c=a[1]["attributes"]
print(c)
print(len(a))
print("Finalizado")


