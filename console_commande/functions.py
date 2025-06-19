import requests
import datetime

API_HOST = "http://10.7.5.148:8000/"


def envoyer_instruction(blocks: list[int], message_label, robot_id):
    """
    Envoie une instruction (liste de blocs) au robot spécifié.

    @param blocks: Liste des identifiants de blocs à envoyer
    @param message_label: Widget Tkinter pour afficher le message de retour
    @param robot_id: Identifiant du robot concerné
    """
    try:
        print(robot_id, blocks)
        payload = {
            "robot_id": robot_id,
            "blocks": blocks,
            "status": "new"
        }

        res = requests.post(f"{API_HOST}/instructions", json=payload)

        if res.status_code == 200:
            afficher_output("Instruction envoyée avec succès", message_label, "green")
        else:
            afficher_output(f"Erreur {res.status_code} : {res.text}", message_label, "red")

    except Exception as e:
        afficher_output(f"Exception : {e}", message_label, "red")


def afficher_instruction(text_output=None, robot_id=None):
    """
    Récupère et affiche l'instruction en cours pour un robot donné.

    @param text_output: Zone de texte Tkinter pour afficher l'instruction
    @param robot_id: Identifiant du robot
    @return: Texte formaté représentant l'instruction ou None
    """
    try:
        res = requests.get(f"{API_HOST}/instructions?robot_id={robot_id}")
        if res.status_code == 200:
            data = res.json()
            if not data.get("success"):
                if text_output:
                    text_output.config(state="normal")
                    text_output.delete("1.0", "end")
                    text_output.insert("end", "Aucune instruction en cours.")
                    text_output.config(state="disabled")
                return None

            blocs = data.get("blocks", [])
            texte_instruction = " - ".join(str(b) for b in blocs)

            if text_output:
                text_output.config(state="normal")
                text_output.delete("1.0", "end")
                text_output.insert("1.0", f"Instruction : {texte_instruction}")
                text_output.config(state="disabled")
            return texte_instruction
        else:
            print(f"Erreur HTTP {res.status_code}")
    except Exception as e:
        print(f"Exception lors de la récupération de l'instruction : {e}")
    return None


def afficher_output(msg, message_label, couleur="black"):
    """
    Affiche un message horodaté dans un widget de texte.

    @param msg: Message à afficher
    @param message_label: Widget Tkinter ciblé
    @param couleur: Couleur du texte
    """
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    message_label.config(text=f"[{timestamp}] {msg}", fg=couleur)


def instruction_en_cours(robot_id: str) -> bool:
    """
    Vérifie si une instruction est en cours pour un robot donné.

    @param robot_id: Identifiant du robot
    @return: True si une instruction est active, False sinon
    """
    try:
        res = requests.get(f"{API_HOST}/instructions/{robot_id}")
        if res.status_code == 200:
            data = res.json()
            return data.get("success", False)
    except Exception as e:
        print(f"Erreur lors de la vérification des instructions : {e}")
    return False


def afficher_telemetrie(zone_telemetrie, robot_id):
    """
    Récupère et affiche les données de télémétrie pour le robot donné.

    @param zone_telemetrie: Widget Tkinter Text où les données seront affichées
    @param robot_id: Identifiant du robot
    """
    try:
        res_instruction = requests.get(f"{API_HOST}/instructions/{robot_id}")
        data = res_instruction.json()

        if not data.get("success", False):
            zone_telemetrie.config(state="normal")
            zone_telemetrie.delete("1.0", "end")
            zone_telemetrie.insert("end", "Aucun ordre en cours pour ce robot.")
            zone_telemetrie.config(state="disabled")
            return

        res = requests.get(f"{API_HOST}/telemetry/{robot_id}")
        if res.status_code == 200:
            donnees = res.json()

            vitesse = donnees.get("vitesse_instant", "N/A")
            distance = donnees.get("ds_ultrasons", "N/A")
            status = donnees.get("status_deplacement", "N/A")
            pince = donnees.get("status_pince", "N/A")
            ligne = donnees.get("ligne", "N/A")

            texte = (
                f"Vitesse : {vitesse}\n"
                f"Distance : {distance} cm\n"
                f"Déplacement : {status}\n"
                f"Pince : {'fermée' if pince else 'ouverte'}\n"
                f"Ligne : {ligne}"
            )

            zone_telemetrie.config(state="normal")
            zone_telemetrie.delete("1.0", "end")
            zone_telemetrie.insert("end", texte)
            zone_telemetrie.config(state="disabled")
        else:
            zone_telemetrie.config(state="normal")
            zone_telemetrie.delete("1.0", "end")
            zone_telemetrie.insert("end", f"Erreur récupération télémétrie : {res.status_code}")
            zone_telemetrie.config(state="disabled")

    except Exception as e:
        zone_telemetrie.config(state="normal")
        zone_telemetrie.delete("1.0", "end")
        zone_telemetrie.insert("end", f"Exception lors de la récupération des données : {e}")
        zone_telemetrie.config(state="disabled")
