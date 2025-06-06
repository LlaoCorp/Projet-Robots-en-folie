# import sys, json, network, urequests, bme280, time, hcsr04 
import time, hcsr04, roues, fonctions_motrices
from machine import Pin, PWM
from fonctions_motrices import *

def test_roues():
    try:
        # mes_roues.avancer()
        # time.sleep(3)
        # mes_roues.reculer()
        # time.sleep(3)
        # mes_roues.gauche()
        # time.sleep(3)
        # mes_roues.droite()
        # time.sleep(3)
        # mes_roues.stop()
        # time.sleep(4)

        if int(distanceMesure()) > 4:
            mes_roues.avancer()
        else:
            mes_roues.stop()
    except KeyboardInterrupt:
        mes_roues.moteur_a(0)
        mes_roues.moteur_b(0)
        print("Arrêt manuel")

def test_pwm():
    in1 = PWM(Pin(26), freq=500, duty=500)
    in2 = PWM(Pin(27), freq=500, duty=500)

# Début de la boucle
while True:
    print(distanceMesure())
    time.sleep(1)
    suivre_ligne(capteur_gauche, capteur_droite)
    cherche_cube()