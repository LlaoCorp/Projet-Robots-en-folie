from tkinter import *
from tkinter import ttk
from functions import *


# Fenêtre plein écran mode immersif
fenetre = Tk()
fenetre.title("Robots en folie")
fenetre.attributes('-fullscreen', True)
fenetre.configure(bg="#f3f4f6")

# Style pour les boutons par défault
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
    font=("Segoe UI", 12),
    background="#3b82f6",
    foreground="white",
    padding=8
)
style.map("TButton",
    background=[("active", "#2563eb")]
)

# Style pour le bouton "mode auto"
style.configure("ModeAuto.TButton",
    font=("Segoe UI", 14, "bold"),
    background="#fbbf24",
    foreground="white",
    padding=10
)
style.map("ModeAuto.TButton",
    background=[("active", "#f59e0b")]
)

# Style pour le bouton "Envoyer texte"
style.configure("SendText.TButton",
    font=("Segoe UI", 10),
    background="#10b981",
    foreground="white",
    padding=5
)
style.map("SendText.TButton",
    background=[("active", "#059669")]
)

# Style pour le bouton Quitter
style.configure("btnQuit.TButton",
    font=("Segoe UI", 10),
    background="#dc2626",
    foreground="white",
    padding=5
)
style.map("btnQuit.TButton",
    background=[("active", "#b91c1c")]
)

# Titre principal
title = Label(fenetre, text="🤖 Robots en folie !", font=("Segoe UI", 36, "bold"), bg="#f3f4f6", fg="#111827")
title.pack(pady=60)

# Conteneur horizontal pour les boutons
frame_btn = Frame(fenetre, bg="#f3f4f6")
frame_btn.pack()

# Liste des boutons avec leurs styles
button_texts = [
    ("Avancer", "TButton", "avancer"),
    ("Reculer", "TButton", "reculer"),
    ("Mode auto", "ModeAuto.TButton", "auto"),
    ("Droite", "TButton", "droite"),
    ("Gauche", "TButton", "gauche")
]

for i, (text, style_name, commande) in enumerate(button_texts):
    btn = ttk.Button(frame_btn, text=text, style=style_name, command=lambda: envoyer_commande(commande, text_output))
    btn.grid(row=0, column=i, padx=20, pady=10, ipadx=10, ipady=5)


btn = ttk.Button(frame_btn, text="Toggle pince", command=lambda: envoyer_commande("toggle_pince", text_output))
btn.grid(row=1, column=2, padx=20, pady=10, ipadx=10, ipady=5)

# Frame pour les zones de texte
text_frame = Frame(fenetre, bg="#f3f4f6")
text_frame.pack(pady=30, fill="both", expand=True)

# Frame pour la zone de gauche (input)
left_box = Frame(text_frame, bg="#f3f4f6")
left_box.pack(side="left", padx=20, fill="both", expand=True)

left_label = Label(left_box, text="Texte à envoyer :", font=("Segoe UI", 12), bg="#f3f4f6", fg="#1f2937")
left_label.pack(anchor="w", pady=(0, 5))  # aligné à gauche
text_input = Text(left_box, width=30, height=10)
text_input.pack(fill="both", expand=True)

btnSendText = ttk.Button(
    left_box,
    text="Envoyer texte",
    style="SendText.TButton",
    command=lambda: envoyer_commande(text_input.get("1.0", "end").strip(), text_output)
)
btnSendText.pack(side="right", padx=5, pady=5)

# Frame pour la zone de droite (output)
right_box = Frame(text_frame, bg="#f3f4f6")
right_box.pack(side="right", padx=20, fill="both", expand=True)

right_label = Label(right_box, text="Réponse du robot :", font=("Segoe UI", 12), bg="#f3f4f6", fg="#1f2937")
right_label.pack(anchor="w", pady=(0, 5))
text_output = Text(right_box, width=30, height=10, state="disabled")
text_output.pack(fill="both", expand=True)

# Frame de bas de page pour placer le bouton quitter correctement
bottom_frame = Frame(fenetre, bg="#f3f4f6")
bottom_frame.pack(side="bottom", fill="x")

btnQuit = ttk.Button(bottom_frame, text="Quitter", command=fenetre.destroy, style="btnQuit.TButton")
btnQuit.pack(side="right", padx=10, pady=10)

# Fermer avec Échap
fenetre.bind("<Escape>", lambda e: fenetre.destroy())

fenetre.mainloop()