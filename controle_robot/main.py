import time, fonctions_motrices, connexion, api_config
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()
already_on = False
apiConf = api_config.ClientAPI('10.7.5.148')

# stop_event = threading.Event() # Crée un événement d'arrêt

derniere_telemetry = time.time()

# def boucle_telemetry():
#     while not stop_event.is_set():
#         print("envoie telemetric")
#         apiConf.envoyer_telemetry(self,
#             get_adr_mac(),
#             distanceMesure(),
#             mes_roues.get_status_deplacement(),
#             (carte_terrain.get_pos_int() + 1),
#             carte_terrain.get_status_pince()
#         )
#         time.sleep(1)

# Lancement du thread secondaire pour la data
# telemetry_thread = threading.Thread(target=boucle_telemetry, daemon=True)
# telemetry_thread.start()

# Début de la boucle
while True:
    # print(distanceMesure())
    try:
        # Gestion de la télémetrie toutes les secondes
        if time.time() - derniere_telemetry >= 1:
            print("envoie telemetric")
            apiConf.envoyer_telemetry(
                get_adr_mac(),
                distanceMesure(),
                mes_roues.get_status_deplacement(),
                (carte_terrain.get_pos_int() + 1),
                carte_terrain.get_status_pince()
            )
            derniere_telemetry = time.time()

        if carte_terrain.get_objectif() != carte_terrain.get_pos():
            already_on = suivre_ligne(already_on)
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
            telemetry_thread.stop()
            break
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")
        time.sleep(3)

# Quand le robot s’arrête, on signale au thread telemetry de s’arrêter
# stop_event.set()
# telemetry_thread.join()  # Attend que le thread se termine proprement
# print("Tout est terminé proprement.")