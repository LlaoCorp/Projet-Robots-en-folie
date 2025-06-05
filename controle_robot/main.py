# import sys, json, network, urequests, bme280, time, hcsr04 
import time, hcsr04 
from machine import Pin, I2C, ADC, deepsleep'

## Mesure l'humidité du sol.
#  @return Entier représentant l'humidité du sol.
def distanceMesure():
    pulsor = hcsr04.HCSR04(5,18)
    distance = pulsor.distance_cm()
    return distance


while True:
    print(distanceMesure())
    time.sleep(1)