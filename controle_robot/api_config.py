import ujson as json
import urequests, time

class ClientAPI:
    def __init__(self, server_ip, port=8000):
        self.base_url = f"http://{server_ip}:{port}"

    def envoyer(self, endpoint, payload):
        try:
            url = self.base_url + endpoint
            headers = {"Content-Type": "application/json"}
            res = urequests.post(url, data=json.dumps(payload), headers=headers)
            # print(f"Requête POST vers {endpoint} - Code : {res.status_code}")
            res.close()
        except Exception as e:
            print("Erreur lors de l'envoi :", e)

    def recuperer_instruction(self, ref_id):
        try:
            url = self.base_url + f"/instructions/{ref_id}"
            res = urequests.get(url)
            if res.status_code == 200:
                data = res.json()
                blocks = data.get("blocks", [])
                print("Instruction reçue :", data)

                self.modifier_statut_instruction(ref_id, "current")
                return blocks
            else:
                print("Erreur récupération instruction - Code :", res.status_code)
            res.close()
        except Exception as e:
            print("Erreur GET instruction :", e)
        return None

    def modifier_statut_instruction(self, ref_id, statut):
        payload = {
            "robot_id": ref_id,
            "status": statut
        }
        self.envoyer(f"/instructions/change_status/{ref_id}", payload)

    def envoyer_telemetry(self, ref_id, ds_ultrasons, statut_deplacement, ligne, statut_pince):
        payload = {
            "robot_id": ref_id,
            "vitesse_instant": 1.0,
            "ds_ultrasons": ds_ultrasons,
            "statut_deplacement": statut_deplacement,
            "ligne": ligne,
            "statut_pince": statut_pince
        }
        self.envoyer("/telemetry", payload)
        time.sleep(1)

    def envoyer_summary(self, ref_id, vitesse_moy):
        payload = {
            "robot_id": ref_id,
            "viesse_moy": vitesse_moy
        }
        self.envoyer("/summary", payload)

    def envoyer_message(self, ref_id, message):
        payload = {
            "robot_id": ref_id,
            "message": message
        }
        self.envoyer("/message", payload)
    
    def recuperer_messages(self, ref_id):
        try:
            url = self.base_url + f"/message/{ref_id}"
            res = urequests.get(url)
            if res.status_code == 200:
                data = res.json()
                messages = data.get("messages", [])
                print("Messages reçus :", messages)
                return messages
            else:
                print("Erreur récupération messages - Code :", res.status_code)
            res.close()
        except Exception as e:
            print("Erreur GET messages :", e)
        return []
