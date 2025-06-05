import machine, time
from machine import Pin, PWM

class Roues:
    def __init__(self, PIN1, PIN2, PIN3, PIN4):
        # ROUES DROITES
        self.IN1 = PWM(Pin(PIN1), freq=1000)
        self.IN2 = PWM(Pin(PIN2), freq=1000)

        # ROUES Gauches
        self.IN3 = PWM(Pin(PIN3), freq=1000)
        self.IN4 = PWM(Pin(PIN4), freq=1000)
    
    # Fonction pour contrôler un moteur
    def moteur_a(self, vitesse):
        if vitesse > 0:
            self.IN1.duty(int(vitesse))
            self.IN2.duty(0)
        elif vitesse < 0:
            self.IN1.duty(0)
            self.IN2.duty(int(-vitesse))
        else:
            self.IN1.duty(0)
            self.IN2.duty(0)

    def moteur_b(self, vitesse):
        if vitesse > 0:
            self.IN3.duty(int(vitesse))
            self.IN4.duty(0)
        elif vitesse < 0:
            self.IN3.duty(0)
            self.IN4.duty(int(-vitesse))
        else:
            self.IN3.duty(0)
            self.IN4.duty(0)

    def avancer(self):
        print("Avancer")
        self.moteur_a(512)  # Valeur PWM entre 0 et 1023
        self.moteur_b(512)
    
    def reculer(self):
        print("Reculer")
        self.moteur_a(-512)
        self.moteur_b(-512)
    
    def stop(self):
        print("Stop")
        self.moteur_a(0)
        self.moteur_b(0)
    
    def droite(self):
        print("Droite")
        self.moteur_a(50)  # Valeur PWM entre 0 et 1023
        self.moteur_b(512)

    def gauche(self):
        print("Gauche")
        self.moteur_a(512)  # Valeur PWM entre 0 et 1023
        self.moteur_b(50)
