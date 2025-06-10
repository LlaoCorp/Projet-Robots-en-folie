# import sys, json, network, urequests, bme280, time, hcsr04 
import time, roues, fonctions_motrices, connexion
from machine import Pin, PWM
from fonctions_motrices import *

def test_pwm():
    in1 = PWM(Pin(26), freq=500, duty=500)
    in2 = PWM(Pin(27), freq=500, duty=500)

connexion.init_connexion()

# Début de la boucle
while True:
    print(distanceMesure())
    try:
        # suivre_ligne()
        test = connexion.request()
        print(test)
        time.sleep(10)
        # cherche_cube()
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")
        time.sleep(3)