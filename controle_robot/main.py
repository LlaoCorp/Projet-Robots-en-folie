# import sys, json, network, urequests, bme280, time, hcsr04 
import time, fonctions_motrices, connexion, api_config
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()
already_on = False
apiConf = api_config.ClientAPI('10.7.5.148')
test = ''

async def boucle_telemetry():
    apiConf.envoyer_telemetry(self,
        get_adr_mac(),
        distanceMesure(),
        mes_roues.get_status_deplacement(),
        (carte_terrain.get_pos_int() + 1),
        carte_terrain.get_status_pince()
    )
    time.sleep(1)

# Début de la boucle
while True:
    boucle_telemetry()
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