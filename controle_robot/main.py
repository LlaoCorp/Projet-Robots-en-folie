# import sys, json, network, urequests, bme280, time, hcsr04 
import time, hcsr04, roues, fonctions_motrices
from machine import Pin, PWM
from fonctions_motrices import *

def distanceMesure():
    pulsor = hcsr04.HCSR04(5,18)
    distance = pulsor.distance_cm()
    return distance

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

def set_angle(angle):
    # Convertit l'angle (0-180) en rapport cyclique (duty)
    min_duty = 26  # correspond à ~0.5ms
    max_duty = 128  # correspond à ~2.5ms
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty(duty)

# Définition des composants
mes_roues = roues.Roues(14,27,26,25)
capteur_gauche = Pin(15, Pin.IN)
capteur_droite = Pin(4, Pin.IN)
servo = PWM(Pin(13), freq=50)

# Début de la boucle
while True:
    print(distanceMesure())
    time.sleep(1)
    suivre_ligne()