import time, hcsr04, roues, carte
from machine import Pin, PWM

# Définition des composants
mes_roues = roues.Roues(14,27,26,25)
capteur_gauche = Pin(15, Pin.IN)
capteur_droite = Pin(4, Pin.IN)
servo = PWM(Pin(13), freq=50)
carte = Carte()

# Fonctions
# ------------

# MOUVEMENTS
def se_retourner():
    # se retourner
    return True

def suivre_ligne():
    if capteur_gauche.value() != 0 and capteur_droite.value() != 0:
        mes_roues.stop()
        print("stop")
    elif capteur_gauche.value() == 0 and capteur_droite.value() == 0:
        mes_roues.avancer()
        print("avance")
    elif capteur_gauche.value() == 0 and capteur_droite.value() != 0:
        mes_roues.droite()
        time.sleep(0.5)
        mes_roues.avancer()
        print("droite")
    else:
        mes_roues.droite()
        time.sleep(0.5)
        mes_roues.avancer()
        print("gauche")

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
    for angle in range(0, 181, 10):
        set_angle(angle)
        time.sleep(0.05)

def lacher_cube():
    for angle in range(180, -1, -10):
        set_angle(angle)
        time.sleep(0.05)

def cherche_cube():
    if int(distanceMesure()) < 4:
        attraper_cube()
    else:
        set_angle(0)