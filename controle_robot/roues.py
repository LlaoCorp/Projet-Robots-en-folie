import machine, time
from machine import Pin, PWM

class Roues:
    def __init__(self, PIN1, PIN2, PIN3, PIN4):
        # ROUES DROITES
        self.IN1 = Pin(PIN1, Pin.OUT)
        self.IN2 = Pin(PIN2, Pin.OUT)

        # ROUES Gauches
        self.IN3 = Pin(PIN3, Pin.OUT)
        self.IN4 = Pin(PIN4, Pin.OUT)

        # Data
        self.status_deplacement = 'stop'
    
    def get_status_deplacement(self):
        return self.status_deplacement

    # Fonction pour contrôler le moteur droit
    def moteur_a(self, vitesse):
        if vitesse < 0:
            self.IN1.value(1)
            self.IN2.value(0)
        elif vitesse > 0:
            self.IN1.value(0)
            self.IN2.value(1)
        else:
            self.IN1.value(0)
            self.IN2.value(0)

    # Fonction pour contrôler le moteur gauche
    def moteur_b(self, vitesse):
        if vitesse < 0:
            self.IN3.value(1)
            self.IN4.value(0)
        elif vitesse > 0:
            self.IN3.value(0)
            self.IN4.value(1)
        else:
            self.IN3.value(0)
            self.IN4.value(0)

    def avancer(self):
        self.moteur_a(1)  # Valeur PWM entre 0 et 1023
        self.moteur_b(1)
        self.status_deplacement = 'avancer'
    
    def reculer(self):
        self.moteur_a(-1)
        self.moteur_b(-1)
        self.status_deplacement = 'reculer'
    
    def stop(self):
        self.moteur_a(0)
        self.moteur_b(0)
        self.status_deplacement = 'stop'
    
    def droite(self):
        self.moteur_a(0)
        self.moteur_b(1)
        self.status_deplacement = 'droite'

    def gauche(self):
        self.moteur_a(1)
        self.moteur_b(0)
        self.status_deplacement = 'gauche'
