import machine, time
from machine import Pin, PWM

class Roues:
    def __init__(self, PIN1, PIN2, PIN3, PIN4, ENA_PIN, ENB_PIN, freq=1000):
        # ROUES DROITES
        self.IN1 = Pin(PIN1, Pin.OUT)
        self.IN2 = Pin(PIN2, Pin.OUT)

        # ROUES GAUCHES
        self.IN3 = Pin(PIN3, Pin.OUT)
        self.IN4 = Pin(PIN4, Pin.OUT)

        # PWM pour vitesse
        self.ENA = PWM(Pin(ENA_PIN), freq=freq)
        self.ENB = PWM(Pin(ENB_PIN), freq=freq)

        # Valeur par défaut de vitesse
        self.vitesse_defaut = 600 # max = 1023

        # État
        self.statut_deplacement = 'stop'
    
    def get_statut_deplacement(self):
        return self.statut_deplacement

    # Contrôle moteur droit
    def moteur_a(self, sens):
        if sens < 0:
            self.IN1.value(1)
            self.IN2.value(0)
            self.ENA.duty(abs(sens))
        elif sens > 0:
            self.IN1.value(0)
            self.IN2.value(1)
            self.ENA.duty(abs(sens))
        else:
            self.IN1.value(0)
            self.IN2.value(0)
            self.ENA.duty(0)

    # Contrôle moteur gauche
    def moteur_b(self, sens):
        if sens < 0:
            self.IN3.value(1)
            self.IN4.value(0)
            self.ENB.duty(abs(sens))
        elif sens > 0:
            self.IN3.value(0)
            self.IN4.value(1)
            self.ENB.duty(abs(sens))
        else:
            self.IN3.value(0)
            self.IN4.value(0)
            self.ENB.duty(0)

    def avancer(self, vitesse=None):
        if vitesse is None:
            vitesse = self.vitesse_defaut
        self.moteur_a(vitesse)
        self.moteur_b(vitesse)
        self.statut_deplacement = 'avancer'
    
    def reculer(self, vitesse=None):
        if vitesse is None:
            vitesse = self.vitesse_defaut
        self.moteur_a(-vitesse)
        self.moteur_b(-vitesse)
        self.statut_deplacement = 'reculer'
    
    def stop(self):
        self.moteur_a(0)
        self.moteur_b(0)
        self.statut_deplacement = 'stop'
    
    def droite(self, vitesse=None):
        if vitesse is None:
            vitesse = self.vitesse_defaut
        self.moteur_a(-50)
        self.moteur_b(vitesse)
        self.statut_deplacement = 'droite'

    def gauche(self, vitesse=None):
        if vitesse is None:
            vitesse = self.vitesse_defaut
        self.moteur_a(vitesse)
        self.moteur_b(-50)
        self.statut_deplacement = 'gauche'