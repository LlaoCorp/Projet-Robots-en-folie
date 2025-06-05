# import sys, json, network, urequests, bme280, time, hcsr04 
import time, hcsr04, roues
from machine import Pin, I2C, ADC, deepsleep

## Mesure l'humidité du sol.
#  @return Entier représentant l'humidité du sol.
def distanceMesure():
    pulsor = hcsr04.HCSR04(5,18)
    distance = pulsor.distance_cm()
    return distance

mes_roues = roues.Roues(14,27,26,25)


while True:
    print(distanceMesure())
    time.sleep(1)
    mes_roues.moteur_a(500)
    
    # if int(distanceMesure()) > 4:
    #     mes_roues.avancer()
    # else:
    #     mes_roues.stop()

    # except KeyboardInterrupt:
    #     moteur_a(0)
    #     moteur_b(0)
    #     print("Arrêt manuel")