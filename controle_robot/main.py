# import sys, json, network, urequests, bme280, time, hcsr04 
import time, roues, fonctions_motrices, connexion
from machine import Pin, PWM
from fonctions_motrices import *
from connexion import *
from fonctions_motrices import carte_terrain

def test_pwm():
    in1 = PWM(Pin(26), freq=500, duty=500)
    in2 = PWM(Pin(27), freq=500, duty=500)

init_connexion()
already_on = False

# Début de la boucle
while True:
    print(distanceMesure())
    try:
        if carte_terrain.get_objectif != carte_terrain.get_pos():
            already_on = suivre_ligne(already_on)
        else:
            carte_terrain.increase_pos()
            # cherche_cube()
        
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")
        time.sleep(3)