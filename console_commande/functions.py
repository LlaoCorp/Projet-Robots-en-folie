import requests
import datetime
import uuid

API_HOST = "http://10.7.5.148:8000/"
ROBOT_ID = ""

def envoyer_instruction(blocks: list[int], text_output, robot_id):
    try:
        payload = {
            "robot_id": robot_id,
            "blocks": blocks,
            "statut": "new"
        }

        res = requests.post(f"{API_HOST}/instructions", json=payload)

        if res.status_code == 200:
            afficher_output("Instruction envoyée avec succès", text_output)
        else:
            afficher_output(f"Erreur {res.status_code} : {res.text}", text_output)

    except Exception as e:
        afficher_output(f"Exception : {e}", text_output)

def afficher_instruction(text_output, robot_id):
    try:
        res = requests.get(f"{API_HOST}/instructions/{robot_id}")
        if res.status_code == 200:
            instruction = res.json()
            afficher_output(f"Instruction actuelle : récupérer les cubes {instruction['blocks']}", text_output)
        else:
            afficher_output(f"Erreur {res.status_code} : {res.text}", text_output)
    except Exception as e:
        afficher_output(f"Exception lors de la lecture de l'instruction : {e}", text_output)

def afficher_output(msg, text_output):
    text_output.config(state="normal")
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    text_output.insert("end", f"[{timestamp}] {msg}\n")
    text_output.see("end")
    text_output.config(state="disabled")

def instruction_en_cours(robot_id: str) -> bool:
    try:
        res = requests.get(f"{API_HOST}/instructions/{robot_id}")
        if res.status_code == 200:
            data = res.json()
            return data.get("success", False)
    except Exception as e:
        print(f"Erreur lors de la vérification des instructions : {e}")
    return False

def afficher_telemetrie(zone_telemetrie, robot_id):
    try:
        res_instruction = requests.get(f"{API_HOST}/instructions/{robot_id}")
        data = res_instruction.json()

        if not data.get("success", False):
            afficher_output("Aucun ordre en cours pour ce robot.", zone_telemetrie)
            return

        res = requests.get(f"{API_HOST}/telemetry/{robot_id}")
        if res.status_code == 200:
            donnees = res.json()

            vitesse = donnees.get("vitesse_instant", "N/A")
            distance = donnees.get("ds_ultrasons", "N/A")
            statut = donnees.get("status_deplacement", "N/A")
            pince = donnees.get("status_pince", "N/A")
            ligne = donnees.get("ligne", "N/A")

            texte = (
                f"Vitesse : {vitesse}\n"
                f"Distance : {distance} cm\n"
                f"Déplacement : {statut}\n"
                f"Pince : {'fermée' if pince else 'ouverte'}\n"
                f"Ligne : {ligne}"
            )

            zone_telemetrie.config(state="normal")
            zone_telemetrie.delete("1.0", "end")
            zone_telemetrie.insert("end", texte)
            zone_telemetrie.config(state="disabled")
        else:
            afficher_output(f"Erreur récupération télémétrie : {res.status_code}", zone_telemetrie)

    except Exception as e:
        afficher_output(f"Exception lors de la récupération des données : {e}", zone_telemetrie)
