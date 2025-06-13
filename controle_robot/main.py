# import sys, json, network, urequests, bme280, time, hcsr04 
import time, fonctions_motrices, connexion
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()
already_on = False
test = ''

# Début de la boucle
while True:
    # print(distanceMesure())
    try:
        if carte_terrain.get_objectif() != carte_terrain.get_pos():
            already_on = suivre_ligne(already_on)
            # if (test != carte_terrain.get_pos()):
            #     test = carte_terrain.get_pos()
            #     print(carte_terrain.get_pos()[0])
        elif carte_terrain.get_pos()[0] == 'c':
            # carte_terrain.increase_pos()
            print("cherche_cube")
            cherche_cube()
            print("fin cherche_cube")
        elif carte_terrain.get_pos() != 'base':
            print("cherche_container")
            cherche_container()
            print("fin cherche_container")
        else:
            mes_roues.stop()
            break
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")
        time.sleep(3)