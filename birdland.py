#pip install requests

import sys
import requests
import csv

class apikeymanager():
    def __init__(self):
        self.f = open("owp_api_key", "r")
        self.key=self.f.read()
        self.f.close()
    def getkey(self):
        return(self.key)

class csvmanager():
         




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

cresp_js=cresp.json()
varos_lat=cresp_js[0]["lat"]
varos_lon=cresp_js[0]["lon"]
print("lat:",varos_lat,"lon:",varos_lon)
wresp= requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+str(varos_lat)+"&lon="+str(varos_lon)+"&exclude=alerts,hourly,daily,current&units=metric&appid="+ak.getkey())
minut=wresp.json()["minutely"]
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