import time, hcsr04, roues, carte
from machine import Pin, PWM

# Définition des composants
mes_roues = roues.Roues(14,27,26,25)
capteur_gauche = Pin(15, Pin.IN)
capteur_droite = Pin(4, Pin.IN)
servo = PWM(Pin(13), freq=50)
carte_terrain = carte.Carte()

# Fonctions
# ------------

# MOUVEMENTS
def se_retourner(side):
    count_lines = 0
    previous_val = 0
    print("tourne")
    while side != carte_terrain.get_reversed():
        mes_roues.droite()
        if count_lines == 2:
            carte_terrain.set_reversed(True)
        if capteur_gauche.value() == 0 or capteur_droite.value() == 0 and previous_val == 1:
            previous_val = 0
            count_lines+=1
        elif capteur_gauche.value() == 1 or capteur_droite.value() == 1:
            previous_val = 1
    print("retourné")

def suivre_ligne(already_on):
    if capteur_gauche.value() != 0 and capteur_droite.value() != 0:
        mes_roues.stop()
        time.sleep(1)
        if already_on == False:
            carte_terrain.increase_pos()
        else:
            mes_roues.avancer()
            time.sleep(1)
        return True
        # se_retourner(False)
        # print("stop")
    elif capteur_gauche.value() == 0 and capteur_droite.value() == 0:
        mes_roues.avancer()
        # print("avance")
    elif capteur_gauche.value() == 0 and capteur_droite.value() != 0:
        mes_roues.stop()
        time.sleep(0.5)
        mes_roues.gauche()
        time.sleep(1)
        # print("gauche")
    else:
        mes_roues.stop()
        time.sleep(0.5)
        mes_roues.droite()
        time.sleep(1)
        # print("droite")
    return False

# FONCTIONS PRATIQUES
def distanceMesure():
    pulsor = hcsr04.HCSR04(5,18)
    distance = pulsor.distance_cm()
    return distance

def set_angle(angle):
    # Convertit un angle (°) en rapport cyclique (duty)
    min_duty = 26  # correspond à ~0.5ms -> 0°
    max_duty = 128  # correspond à ~2.5ms -> 180°
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty)) # Calcul inspiré de ChatGPT
    servo.duty(duty)

# FONCTIONS DU CUBE
def attraper_cube():
    # for angle in range(0, 181, 10):
    #     set_angle(angle)
    #     time.sleep(0.05)
    # set_angle(45)
    # time.sleep(3)
    set_angle(90)
    time.sleep(3)

def lacher_cube():
    # for angle in range(180, -1, -10):
    #     set_angle(angle)
    #     time.sleep(0.5)
    # set_angle(135)
    # time.sleep(3)
    set_angle(180)
    time.sleep(3)

def cherche_cube():
    # Se cadrer
    mes_roues.reculer()
    time.sleep(1)
    mes_roues.droite()
    time.sleep(1)

    # Boucle pour ce mettre à la bonne distance du cube
    while int(distanceMesure()) > 2 or int(distanceMesure()) < 1:
        if int(distanceMesure()) > 2:
            mes_roues.avancer()
        elif int(distanceMesure()) < 1:
            mes_roues.reculer()
        else:
            break
    attraper_cube()
    
    # Se remettre sur la ligne
    mes_roues.gauche()
    time.sleep(1)
    mes_roues.reculer()
    time.sleep(1)
    carte_terrain.set_objectif(carte_terrain.get_best_container())

def cherche_container():
    # if carte_terrain.get_pos()[0] == 'e':

    # On centre
    mes_roues.avancer()
    time.sleep(1.5)
    # On va dans la zone
    mes_roues.droite()
    time.sleep(1)
    mes_roues.avancer()
    time.sleep(1)
    mes_roues.stop()
    lacher_cube()
    # On reviens sur la ligne
    mes_roues.reculer()
    time.sleep(1)
    mes_roues.gauche()
    time.sleep(1)
    mes_roues.stop()
    
    carte_terrain.set_objectif('base')

    # elif carte_terrain.get_pos()[0] == 's':
    #     # On centre
    #     mes_roues.avancer()
    #     time.sleep(1.5)
    #     # On va dans la zone
    #     mes_roues.gauche()
    #     time.sleep(1)
    #     mes_roues.stop()
    #     lacher_cube()
    #     # On reviens sur la ligne
    #     mes_roues.droite()
    #     time.sleep(1)
    #     mes_roues.stop()
    # else:
    #     print("erreur de position")


def test_servo2():
    set_angle(45)
    print(45)
    time.sleep(3)
    
    set_angle(90)
    print(90)
    time.sleep(3)

    set_angle(135)
    print(135)
    time.sleep(3)

    set_angle(180)
    print(180)
    time.sleep(3)
    #wait
    time.sleep(5)