#pip install requests

import sys
import requests
import csv
import datetime
from datetime import datetime

class apikeymanager():
    def __init__(self):
        self.f = open("owp_api_key", "r")
        self.key=self.f.read()
        self.f.close()
    def getkey(self):
        return(self.key)

class csvmanager():
    def __init__(self):
        print()

    def read_current():
        print()

    def write_current():
        print()
    def check_in_current():
        print()
    def write_log(self,varos,lat,lon,n1,n2,n3):
        print()
       

class logtofile:
    def __init__(self,logfilenev):
        self.fl = open(logfilenev+".csv","a")

    def write(self,varos,lat,lon,n1,n2,n3,n4):
        self.fl.write(datetime.now().strftime("%y.%m.%d %H.%M:%S")+","+varos+","+str(lat)+","+str(lon)+","+str(n1)+","+str(n2)+","+str(n3)+","+str(n4)+chr(13))
        
    
    def close(self):
        self.fl.close()

    


         




#------------------
# Main
#------------------

ak=apikeymanager()
"""
if len(sys.argv)!=2:
    print("Használat: python birdland.py településnév országkód (Ha nem ír országkódot, akkor az automatikusan hu")
    print("pl: python birdland.py Budapest (Magyarország fővárosa) vagy python birdland.py Budapest,us (Egy kisváros az USA-ban)")
    #exit()
varos=sys.argv[1] """
varos="Dunaújváros"
if varos[-3:-2]!=",":
    varos=varos+",hu"
print(varos)
cresp=requests.get("http://api.openweathermap.org/geo/1.0/direct?q="+varos+"&limit=1&appid="+ak.getkey())
print("cresp status code:",cresp.status_code)
if cresp.status_code!=200:
    print("Hiba az openweathermap api lekérdezésnél. Város lekérdezés. Státusz kód: ",cresp.status_code)
    exit()
cresp_js=cresp.json()
varos_lat=cresp_js[0]["lat"]
varos_lon=cresp_js[0]["lon"]
print("lat:",varos_lat,"lon:",varos_lon)
wresp= requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+str(varos_lat)+"&lon="+str(varos_lon)+"&exclude=alerts,hourly,daily,current&units=metric&appid="+ak.getkey())
minut=wresp.json()["minutely"]
print("wresp status code:",wresp.status_code)
if wresp.status_code!=200:
    print("Hiba az openweathermap api lekérdezésnél. Előrejelzés lekérdezés. Státusz kód: ",wresp.status_code)
    exit()
n1=n2=n3=n4=0
i=0
while i<=14:
    n1=n1+minut[i]["precipitation"]
    n2=n2+minut[i+15]["precipitation"]
    n3=n3+minut[i+30]["precipitation"]
    n4=n4+minut[i+45]["precipitation"]
    i=i+1
print("Az eső mennyisége mm-ben negyedóránkénti bontásban:")
print("1.",n1)
print("2.",n2)
print("3.",n3)
print("4.",n4)

csvlog=logtofile("rainlog")
csvlog.write(varos,varos_lat,varos_lon,n1,n2,n3,n4)
csvlog.close()
