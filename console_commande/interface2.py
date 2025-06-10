import tkinter as tk
from tkinter import ttk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Contrôle Robot Suiveur de Ligne")
root.geometry("400x350")
root.resizable(False, False)

# Style moderne avec ttk
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 12), padding=10)
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TFrame", background="#f0f0f0")

# Cadre principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Étiquette de titre
title_label = ttk.Label(main_frame, text="Interface de contrôle", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=(0, 20))

# Boutons de contrôle
btn_start = ttk.Button(main_frame, text="Démarrer le robot")
btn_start.pack(pady=5)

btn_stop = ttk.Button(main_frame, text="Arrêter le robot")
btn_stop.pack(pady=5)

btn_sensor = ttk.Button(main_frame, text="Lire capteur")
btn_sensor.pack(pady=5)

btn_status = ttk.Button(main_frame, text="Obtenir l'état")
btn_status.pack(pady=5)

# Zone de statut (résultats / messages)
status_label = ttk.Label(main_frame, text="État : Non connecté", foreground="gray")
status_label.pack(pady=(30, 5))

# Champ de texte pour afficher les réponses
result_box = tk.Text(main_frame, height=5, wrap="word", font=("Segoe UI", 10))
result_box.pack(fill=tk.X)

# Boucle principale
root.mainloop()
