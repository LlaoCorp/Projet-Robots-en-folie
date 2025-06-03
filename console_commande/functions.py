import requests
import datetime

API_URL = "http://localhost:8000/envoyer/"  # correspond à ton endpoint POST

def envoyer_commande(commande, text_output):
    try:
        data = {
            "robot_id": "1234-uuid",  # à adapter selon ton modèle Pydantic
            "contenu": commande
        }

        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            resultat = response.json()
            afficher_output(f"✅ {resultat['message']}", text_output)
        else:
            afficher_output(f"❌ Erreur : {response.status_code}", text_output)
    except Exception as e:
        afficher_output(f"⚠️ Exception : {e}", text_output)


def afficher_output(msg, text_output):
    text_output.config(state="normal")
    text_output.insert("end", f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    text_output.see("end")
    text_output.config(state="disabled")