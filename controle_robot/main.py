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
objectif = 'c1'
print(carte_terrain.get_pos())

# Début de la boucle
while True:
    print(distanceMesure())
    try:
        if objectif != carte_terrain.get_pos():
            suivre_ligne()
        else:
            test_servo2()
        # test = request()
        # print(test.status_code, test.text)
        # cherche_cube()
        
    except KeyboardInterrupt:
        mes_roues.stop()
        print("Arrêt manuel")
        time.sleep(3)