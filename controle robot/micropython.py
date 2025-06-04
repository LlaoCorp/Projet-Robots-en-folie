# import sys, json, network, urequests, bme280, time, hcsr04 
import time, hcsr04 
#from machine import Pin, I2C, ADC, deepsleep

## Configuration de la connexion Wi-Fis
ssid = 'IMERIR Fablab'
password = 'imerir66'
id = 'ed3029a5-ed9c-4599-bef0-fed1bf78badb'

## Mesure l'humidité du sol.
#  @return Entier représentant l'humidité du sol.
def distanceMesure():
    pulsor = hcsr04.HCSR04(5,18)
    distance = pulsor.distance_cm()
    return distance


while True:
    print(distanceMesure())
    time.sleep(0.5)