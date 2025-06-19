import time, fonctions_motrices, connexion, builtins
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()

already_on = False
mes_roues.stop()

get_instructions()

# Début de la boucle
while True:
    try:
        if carte_terrain.get_objectif() != carte_terrain.get_pos():
            already_on = suivre_ligne(already_on)
        elif carte_terrain.get_pos()[0] == 'c':
            send_telemetry("cherche_cube")
            cherche_cube()
            send_telemetry("fin cherche_cube")
        elif carte_terrain.get_pos() != 'base':
            send_telemetry("cherche_container")
            cherche_container()
            send_telemetry("fin cherche_container")
        else:
            send_telemetry("retour à la base")
            mes_roues.stop()
            break
    except KeyboardInterrupt:
        mes_roues.stop()
        send_telemetry("Arrêt manuel")
        if carte_terrain.get_statut_pince() == True :
            attraper_cube()
        time.sleep(3)
