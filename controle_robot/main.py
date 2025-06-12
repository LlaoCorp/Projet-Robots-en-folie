# import sys, json, network, urequests, bme280, time, hcsr04 
import time, fonctions_motrices, connexion
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()
already_on = False

# Début de la boucle
while True:
    print(distanceMesure())
    try:
        if carte_terrain.get_objectif != carte_terrain.get_pos():
            already_on = suivre_ligne(already_on)
        elif carte_terrain.get_pos[0] == 'c':
            carte_terrain.increase_pos()
            # cherche_cube()
        elif carte_terrain.get_pos != 'base':
            # cherche_container()
            print("cherche_container")
        else:
            mes_roues.stop()
            break
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")
        time.sleep(3)