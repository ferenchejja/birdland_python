# birdland
Időjárásjelentés openweatermap api-val

Használat:

python birdland.py településnév,országkód (Ha nem ír országkódot, akkor az automatikusan hu lesz.)

pl:

python birdland.py Budapest    #Magyarország fővárosa

vagy 

python birdland.py Budapest,us  #Egy kisváros az USA-ban

A program kiírja az https://openweathermap.org/ adatai alapján, hogy az elkövetkező egy órában az adott városban mennyi eső fog esni, negyedórás bontásban.

20 percen belüli ismételt lekérdezésnél a tárolt adatot adja vissza, ha mindenképp a friss adatot szeretné lekérni, használja a -friss paramétert

pl: python birdland.py Budapest -friss 


Első futtatás előtt installálni kell a szükséges csomagokat:

pip install -r requirements.txt