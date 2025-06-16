from tkinter import *
from tkinter import ttk
from functions import envoyer_instruction, afficher_instruction, afficher_telemetrie, instruction_en_cours

boucle_active = True

# Fenêtre plein écran mode immersif
fenetre = Tk()
fenetre.title("Robots en folie")
fenetre.attributes('-fullscreen', True)
fenetre.configure(bg="#f3f4f6")

# Styles
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 12), background="#3b82f6", foreground="white", padding=8)
style.map("TButton", background=[("active", "#2563eb")])

style.configure("SendText.TButton", font=("Segoe UI", 10), background="#10b981", foreground="white", padding=5)
style.map("SendText.TButton", background=[("active", "#059669")])

style.configure("btnQuit.TButton", font=("Segoe UI", 10), background="#dc2626", foreground="white", padding=5)
style.map("btnQuit.TButton", background=[("active", "#b91c1c")])

# Titre principal
title = Label(fenetre, text="🤖 Robots en folie !", font=("Segoe UI", 36, "bold"), bg="#f3f4f6", fg="#111827")
title.pack(pady=60)

# Frame mission
frame_mission = Frame(fenetre, bg="#f3f4f6")
frame_mission.pack(pady=10)

label_robot_id = Label(frame_mission, text="ID du robot", font=("Segoe UI", 12), bg="#f3f4f6")
label_robot_id.grid(row=1, column=0, padx=5, pady=5)

entry_robot_id = Entry(frame_mission, font=("Segoe UI", 12), width=30)
entry_robot_id.grid(row=1, column=1, padx=5, pady=5)

# label_mission = Label(frame_mission, text="Liste de blocs (séparés par des virgules)", font=("Segoe UI", 12), bg="#f3f4f6")
# label_mission.grid(row=0, column=0, padx=5)

# entry_blocs = Entry(frame_mission, font=("Segoe UI", 12), width=30)
# entry_blocs.grid(row=0, column=1, padx=5)

# Couleurs et blocs associés
couleurs_blocs = {
    "Jaune": 2,
    "Rouge": 3,
    "Rose": 6,
    "Violet": 7,
    "Vert": 10
}
selections = {couleur: BooleanVar() for couleur in couleurs_blocs}

# Affichage des cases à cocher
row_index = 2
for i, (couleur, var) in enumerate(selections.items()):
    check = Checkbutton(frame_mission, text=couleur, variable=var, bg="#f3f4f6", font=("Segoe UI", 12))
    check.grid(row=row_index, column=i % 2, padx=10, pady=2, sticky="w")
    if i % 2 == 1:
        row_index += 1

# Zone de texte de sortie
# text_output = Text(fenetre, height=5, bg="white", font=("Consolas", 11), wrap="word", state="disabled")
# text_output.pack(padx=30, pady=20, fill="both", expand=True)

message_label = Label(fenetre, text="", font=("Segoe UI", 12), bg="#f3f4f6", fg="#111827")
message_label.pack(pady=10)

# Bouton : Envoyer mission
def bouton_envoyer_instruction():
    robot_id = entry_robot_id.get().strip()
    if robot_id:
        blocs = [valeur for couleur, valeur in couleurs_blocs.items() if selections[couleur].get()]
        if blocs:
            envoyer_instruction(blocs, message_label, robot_id)
        else:
            message_label.config(text="Aucun bloc sélectionné.", fg="red")
    else:
        message_label.config(text="Veuillez entrer un ID de robot.", fg="red")

# Création du bouton
btnSendMission = ttk.Button(
    frame_mission,
    text="Envoyer mission",
    style="SendText.TButton",
    command=bouton_envoyer_instruction
)
btnSendMission.grid(row=0, column=2, padx=10)

def button_afficher_instruction():
    robot_id = entry_robot_id.get().strip()
    if robot_id:
        instruction = afficher_instruction(None, robot_id)
        if instruction:
            message_label.config(text=f"Mission : {instruction}", fg="green")
        else:
            message_label.config(text="Aucune instruction trouvée.", fg="orange")
    else:
        message_label.config(text="Veuillez entrer un ID de robot.", fg="red")

# Bouton : Voir mission
btnVoirMission = ttk.Button(
    frame_mission,
    text="Voir mission actuelle",
    style="TButton",
    command=button_afficher_instruction
)
btnVoirMission.grid(row=0, column=3, padx=10)

def bouton_sauvegarder_robot():
    robot_id = entry_robot_id.get().strip()
    if robot_id:
        boucle_rafraichissement()
    else:
        message_label.config(text="Veuillez entrer un ID de robot.", fg="red")

# Bouton : Voir mission
btnSaveRobot = ttk.Button(
    frame_mission,
    text="Sauvegarder robot",
    style="SendText.TButton",
    command=bouton_sauvegarder_robot
)
btnSaveRobot.grid(row=1, column=2, padx=10)

# Cadre d'affichage de la télémétrie
frame_telemetrie = Frame(fenetre, bg="#f3f4f6")
frame_telemetrie.pack(padx=30, pady=10, fill="x")

label_telemetrie = Label(frame_telemetrie, text="📡 Données de télémétrie :", font=("Segoe UI", 12, "bold"), bg="#f3f4f6")
label_telemetrie.pack(anchor="w")

zone_telemetrie = Text(frame_telemetrie, height=7, font=("Consolas", 10), bg="white", state="disabled")
zone_telemetrie.pack(fill="x", pady=5)

# Frame de bas de page pour placer le bouton quitter correctement
bottom_frame = Frame(fenetre, bg="#f3f4f6")
bottom_frame.pack(side="bottom", fill="x")

btnQuit = ttk.Button(bottom_frame, text="Quitter", command=fenetre.destroy, style="btnQuit.TButton")
btnQuit.pack(side="right", padx=10, pady=10)

# Fermer avec Échap
fenetre.bind("<Escape>", lambda e: fenetre.destroy())

def boucle_rafraichissement():
    robot_id = entry_robot_id.get().strip()
    if instruction_en_cours(robot_id):
        boucle_active = True
        afficher_telemetrie(zone_telemetrie, robot_id)
        if boucle_active:
            fenetre.after(1000, boucle_rafraichissement)
    else:
        boucle_active = False
        message_label.config(text="Aucune mission en cours pour ce robot", fg="red")
    
fenetre.mainloop()