import os
import sys
import requests
import csv
import datetime
from datetime import datetime

class get_api_key():
    def __init__(self):
        self.f = open("owp_api_key", "r")
        self.key=self.f.read()
        self.f.close()
    def getkey(self):
        return(self.key)


class logtofile:
    def __init__(self,logfilenev):
        self.fl = open(logfilenev+".csv","a")

    def write(self,varos,lat,lon,n1,n2,n3,n4):
        self.fl.write(datetime.now().strftime("%y.%m.%d %H.%M:%S")+f",{varos},{lat},{lon},{n1},{n2},{n3},{n4}"+chr(13))
      
    
    def close(self):
        self.fl.close()


class check_in_log:
    def __init__(self,logfilenev,varos):
        self.fl = open(logfilenev+".csv","r")
        csv_reader=csv.reader(self.fl)
        delta=1200
        self.foundincache=False
        for row in csv_reader:
            timedelta=(datetime.now()-datetime.strptime(row[0],"%y.%m.%d %H.%M:%S")).total_seconds()
            if (datetime.now()-datetime.strptime(row[0],"%y.%m.%d %H.%M:%S")).total_seconds()<delta and varos==row[1]+","+row[2]:
                self.varos_timestamp=row[0]
                self.varos=row[1]+","+row[2]
                self.varos_lon=row[3]
                self.varos_lat=row[4]
                self.n1=row[5]
                self.n2=row[6]
                self.n3=row[7]
                self.n4=row[8]
                self.foundincache=True
                self.timedelta=timedelta

        self.fl.close()

    def found(self):
       return self.foundincache

#------------------
# Main
#------------------

if __name__ == "__main__":
    ak=get_api_key()
    logfilename="rainlog"
    if not os.path.isfile("./"+logfilename+".csv"):
        newfile=open(logfilename+".csv","w")
        newfile.close()

    print("Csapadék a következő órában negyedórás bontásban.")
    print()
    if len(sys.argv)<2 or len(sys.argv)>3:
        print("Használat: python birdland.py településnév országkód (Ha nem ír országkódot, akkor az automatikusan hu")
        print("pl: python birdland.py Budapest (Magyarország fővárosa) vagy python birdland.py Budapest,us (Egy kisváros az USA-ban)")
        print()
        print("20 percen belüli ismételt lekérdezésnél a tárolt adatot adja vissza, ha mindenképp a friss adatot szeretné lekérni, használja a -friss paramétert")
        print("pl: python birdland.py Budapest -friss ")
        exit()
    varos=sys.argv[1] 
    if varos[-3:-2]!=",":
        varos=varos+",hu"
    print(varos)
    forcedfresh=False
    if len(sys.argv)==3:
        if sys.argv[2]=="-friss":
            forcedfresh=True
    if forcedfresh:
        foundincache=False
    else:
        cl=check_in_log(logfilename,varos)
        foundincache=cl.foundincache

    if foundincache:
        varos_timestamp=cl.varos_timestamp
        varos_lon=cl.varos_lon
        varos_lat=cl.varos_lat
        n1=float(cl.n1)
        n2=float(cl.n2)
        n3=float(cl.n3)
        n4=float(cl.n4)
    else:
        cityresp=requests.get("http://api.openweathermap.org/geo/1.0/direct?q="+varos+"&limit=1&appid="+ak.getkey())
        if cityresp.status_code!=200:
            print("Hiba az openweathermap api lekérdezésnél. Város lekérdezés. Státusz kód: ",cityresp.status_code)
            exit()
        cresp_js=cityresp.json()
        if cresp_js==[]:
            print("Nincs ilyen város!")
            exit()
        varos_lat=cresp_js[0]["lat"]
        varos_lon=cresp_js[0]["lon"]
        weatherresp= requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+str(varos_lat)+"&lon="+str(varos_lon)+"&exclude=alerts,hourly,daily,current&units=metric&appid="+ak.getkey())
        minut=weatherresp.json()["minutely"]
        if weatherresp.status_code!=200:
            print("Hiba az openweathermap api lekérdezésnél. Előrejelzés lekérdezés. Státusz kód: ",weatherresp.status_code)
            exit()
        n1=n2=n3=n4=0
        i=0
        while i<=14:
            n1=n1+minut[i]["precipitation"]
            n2=n2+minut[i+15]["precipitation"]
            n3=n3+minut[i+30]["precipitation"]
            n4=n4+minut[i+45]["precipitation"]
            i=i+1

    if foundincache==True:
        print("Tárolt adat! Lekérdezés ideje:",varos_timestamp)
        print(f"Lekérdezés óta eltelt idő: {cl.timedelta:.2f} másodperc")
    else:
        print("Friss adat! Lekérdezés ideje:", (datetime.now()).strftime("%y.%m.%d %H.%M:%S"))
    print("lat:",varos_lat,"lon:",varos_lon)
    print("Az eső mennyisége mm-ben negyedóránkénti bontásban:")
    print(f"1.: {n1:.3f} mm   2.: {n2:.3f} mm   3.: {n3:.3f} mm   4.: {n4:.3f} mm ")

    csvlog=logtofile(logfilename)
    csvlog.write(varos,varos_lat,varos_lon,n1,n2,n3,n4)
    csvlog.close()
