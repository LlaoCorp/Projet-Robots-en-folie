import time, hcsr04, roues, carte, builtins
from machine import Pin, PWM

# Définition des composants
mes_roues = roues.Roues(14,27,26,25,32,33) # Définition des roues
capteur_gauche = Pin(15, Pin.IN)        # Définition du capteur de ligne gauche
capteur_droite = Pin(4, Pin.IN)         # Définition du capteur de ligne droite
servo = PWM(Pin(13), freq=50)           # Définition du servo moteur (pince)
carte_terrain = carte.Carte()           # Définition de la carte contenant le trajet du robot

# Fonctions
# ------------

# MOUVEMENTS
##
def se_retourner(side):
    """! se_retourner permet au robot de se retourner pour retracer son chemin jusqu'au container précédent.

    @param side Le sense dans lequel le robot se trouve
    """ 
    count_lines = 0
    print("tourne")
    while side != carte_terrain.get_reversed():
        mes_roues.droite(800)
        if count_lines == 2:
            carte_terrain.set_reversed(True)

        if capteur_gauche.value() != 0:
            count_lines += 1
            time.sleep(0.3)
    print("retourné")

def suivre_ligne(already_on, apiConf):
    """! Permet de suivre la ligne et de repèrer les checkpoints.

    @param already_on Boolean permettant de definir si le robot est toujours sur la ligne ou non. 
    @return True, si le robot repère un "checkpoint", sinon False
    """ 
    if capteur_gauche.value() != 0 and capteur_droite.value() != 0:
        mes_roues.stop()
        time.sleep(0.2)
        if already_on == False:
            carte_terrain.increase_pos()
            apiConf.envoyer_message('72a1834d-98ef-4b46-87f5-5e4c4e82e39a', carte_terrain.get_pos())
        else:
            mes_roues.avancer(1000)
            time.sleep(0.5)
        return True
    elif capteur_gauche.value() == 0 and capteur_droite.value() == 0:
        mes_roues.avancer()
        time.sleep(0.01)
    elif capteur_gauche.value() == 0 and capteur_droite.value() != 0:
        print('capteur droite')
        mes_roues.stop()
        time.sleep(0.2)
        mes_roues.gauche(900)
        time.sleep(0.2)
    elif capteur_gauche.value() != 0 and capteur_droite.value() == 0:
        print('capteur gauche')
        mes_roues.stop()
        time.sleep(0.2)
        mes_roues.droite(800)
        time.sleep(0.2)
    return False

# FONCTIONS PRATIQUES
def distanceMesure():
    """! Permet de suivre la ligne et de repèrer les checkpoints.
 
    @return la distance entre le capteur et l'obstacle en face.
    """ 
    pulsor = hcsr04.HCSR04(5,18)
    distance = pulsor.distance_cm()
    return distance

def set_angle(angle):
    """! Permet de convertir un angle (°) en rapport cyclique (duty). """
    min_duty = 26  # correspond à ~0.5ms -> 0°
    max_duty = 128  # correspond à ~2.5ms -> 180°
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty)) # Calcul inspiré de ChatGPT
    servo.duty(duty)

# FONCTIONS DU CUBE
def attraper_cube():
    """! Permet de refermer la pince. """
    set_angle(180)
    time.sleep(3)
    carte_terrain.set_statut_pince(False)

def lacher_cube():
    """! Permet d'ouvrir la pince. """
    set_angle(90)
    time.sleep(3)
    carte_terrain.set_statut_pince(True)

def cherche_cube():
    """! Permet de trouver le cube, le prendre puis, revenir sur la ligne. """
    # Se cadrer
    mes_roues.reculer(700)
    time.sleep(0.6)
    print("fin recule")

    # Trouver le cube
    while int(distanceMesure()) > 20 or int(distanceMesure()) < 1:
        mes_roues.gauche(800)
        time.sleep(0.1)
        mes_roues.stop()
        time.sleep(0.1)
    mes_roues.stop()
    lacher_cube() # On ouvre les pinces
    print("cube trouvé")

    # Boucle pour se mettre à la bonne distance du cube
    while int(distanceMesure()) > 2 or int(distanceMesure()) < 1:
        if int(distanceMesure()) > 2 or int(distanceMesure()) < 0:
            mes_roues.avancer()
        elif int(distanceMesure()) < 1:
            mes_roues.reculer()
        else:
            break
        time.sleep(0.1)
        mes_roues.stop()
    print("sur le cube")

    attraper_cube() # On attrape le cube une fois que l'on est bien aligné
    
    # Se remettre sur la ligne
    while capteur_droite.value() != 0:
        mes_roues.reculer(800)
        time.sleep(0.1)
    mes_roues.droite(800)
    time.sleep(0.5)
    mes_roues.stop()
    print("Sur la ligne")
    carte_terrain.set_objectif(carte_terrain.get_best_container())

def cherche_container():
    """! Permet de trouver un container, y poser le cube puis, revenir sur la ligne. """
    # if carte_terrain.get_pos()[0] == 'e':

    # On previent
    mes_roues.stop()
    time.sleep(1)

    # On centre
    mes_roues.avancer()
    time.sleep(1)

    # On va dans la zone
    mes_roues.gauche(1000)
    time.sleep(0.7)
    mes_roues.avancer(1000)
    time.sleep(0.5)
    mes_roues.stop()
    lacher_cube()

    # On reviens sur la ligne
    while capteur_droite.value() != 0:
        mes_roues.reculer(800)
        time.sleep(0.1)
    mes_roues.droite(800)
    time.sleep(0.5)
    mes_roues.stop()
    attraper_cube()

    # On mets les objectifs à jour
    carte_terrain.delete_prev_objectif()
    if len(carte_terrain.get_objectif_list()) > 0:
        carte_terrain.set_objectif(carte_terrain.get_objectif_list()[0])
    else:
        carte_terrain.set_objectif('base')