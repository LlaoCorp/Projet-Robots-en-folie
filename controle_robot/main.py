import time, fonctions_motrices, connexion, api_config, builtins
from fonctions_motrices import *
from fonctions_motrices import carte_terrain, mes_roues
from connexion import *

init_connexion()
apiConf = api_config.ClientAPI('10.7.5.148')
already_on = False
instruction_getted = False

uuid = '72a1834d-98ef-4b46-87f5-5e4c4e82e39a'

debug_mode = False
mes_roues.stop()

# Boucle pour la récupération d'instruction envoyé par le server
while instruction_getted == False:
    if debug_mode == True:
        break
    time.sleep(1)
    print('waiting for return...')
    blocks = apiConf.recuperer_instruction(uuid)

    # if blocks is not None and builtins.len(blocks) != 0:
    if blocks is not None:
        carte_terrain.set_objectif_by_int(blocks)
        print(carte_terrain.get_objectif_list())
        instruction_getted == True
        break

# derniere_telemetry = time.time()
# Gestion de la télémetrie toutes les secondes
def send_telemetry(message=""):
    apiConf.envoyer_telemetry(
        uuid,
        distanceMesure(),
        mes_roues.get_statut_deplacement(),
        (carte_terrain.get_pos_int() + 1),
        carte_terrain.get_statut_pince()
    )
    if message != "":
        apiConf.envoyer_message(uuid, message)

# Début de la boucle
if debug_mode != True:
    while True:
        try:
            # if time.time() - derniere_telemetry >= 1:
            #     send_telemetry()
            #     derniere_telemetry = time.time()

            if carte_terrain.get_objectif() != carte_terrain.get_pos():
                already_on = suivre_ligne(already_on, apiConf)
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

test = ''
while True:
    if debug_mode == False:
        break
    test = input("quoi moi faire?")
    if test == '0':
        mes_roues.stop()
        break
    elif test == '1':
        mes_roues.avancer()
    elif test == '2':
        mes_roues.stop()
    elif test == '3':
        lacher_cube()
    elif test == '4':
        attraper_cube()
    elif test == '5':
        mes_roues.reculer()