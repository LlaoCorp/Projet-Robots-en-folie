# import sys, json, network, urequests, bme280, time, hcsr04 
import time, hcsr04, roues, fonctions_motrices
from machine import Pin, PWM
from fonctions_motrices import *

def test_pwm():
    in1 = PWM(Pin(26), freq=500, duty=500)
    in2 = PWM(Pin(27), freq=500, duty=500)

# Début de la boucle
while True:
    print(distanceMesure())
    time.sleep(1)
    try:
        suivre_ligne(capteur_gauche, capteur_droite)
        cherche_cube()
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")