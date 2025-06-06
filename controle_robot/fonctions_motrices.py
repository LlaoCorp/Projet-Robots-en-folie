def suivre_ligne():
    if capteur_gauche.value() != 0 and capteur_droite.value() != 0:
        print("stop")
    elif capteur_gauche.value() == 0 and capteur_droite.value() == 0:
        print("avance")
    elif capteur_gauche.value() == 0 and capteur_droite.value() != 0:
        print("aller légèrement à droite") # genre droite->wait->avance
    else:
        print("aller légèrement à gauche") # genre gauche->wait->avance

# FONCTIONS DU CUBE
def attraper_cube():
    for angle in range(0, 181, 10):
        set_angle(angle)
        time.sleep(0.05)

def lacher_cube():
    for angle in range(180, -1, -10):
        set_angle(angle)
        time.sleep(0.05)

def cherche_cube():
    if int(distanceMesure()) < 4:
        attraper_cube()
    else:
        set_angle(0)