import time, fonctions_motrices, connexion, api_config
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()
apiConf = api_config.ClientAPI('10.7.5.148')
already_on = False
instruction_getted = False

# Boucle pour la récupération d'instruction envoyé par le server
while instruction_getted == False:
    print('test 2')
    time.sleep(1)
    print('waiting for return...')
    blocks = apiConf.recuperer_instruction(get_adr_mac())
    if blocks != None and len(blocks) != 0:
        carte_terrain.set_objectif_by_int = blocks
        print(carte_terrain.get_objectif)
        instruction_getted == True

derniere_telemetry = time.time()

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
            print(
                get_adr_mac(),
                distanceMesure(),
                mes_roues.get_status_deplacement(),
                (carte_terrain.get_pos_int() + 1),
                carte_terrain.get_status_pince())
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